import datetime
import re
from uuid import uuid4

import sqlalchemy as sa
from google.auth.transport import requests
from google.oauth2 import id_token
from itsdangerous import BadData, SignatureExpired, URLSafeTimedSerializer
from quart import Blueprint, current_app, request
from quart import session as otp_session
from quart_auth import current_user, login_required, login_user, logout_user
from quart_schema import validate_request, validate_response

from db_access.account_lockout import delete_lockout, get_lockout
from db_access.device import add_logged_in_device, remove_logged_in_device
from db_access.failed_attempt import delete_failed_attempt
from db_access.globals import async_session
from db_access.otp import create_otp, delete_otp, get_otp
from db_access.user import get_user_details, insert_user_by_google
from models import AuthedUser, User
from models.general.BrowsingData import BrowsingData
from models.request_data import (
    ForgotPasswordBody,
    LoginBody,
    LoginCallBackBody,
    OTPBody,
    ResetPasswordBody,
    SignUpBody
)
from models.response_data import UserData
from security_functions.cryptography import pw_hash, pw_verify
from utils.logging import log_info, log_warning
from .functions import (
    generate_otp,
    get_location_from_ip,
    get_user_agent_data,
    send_otp_email,
    send_password_recovery_email,
    evaluate_failed_attempts
)

FORGET_PASSWORD_SALT = b'\x80\x1c\rqn\xb2\x7f\x03\x90\xeeA\x18ex\x0e\xc1\x14\xf7\xf3A\x8b\xbc\\]\x1ag\xd8\xcbk\xd3\x9a\x9a3\xce\x14\xbe\xc7\x1ak^K>\xb5jyu,:\xdaF\xc2\x08\xae5\xcf$\x90M[\xcd&\xc1\x90\x06\xa5i\x81\xfd70\xd3\x1d\x03\x06\xf4(Up6\x08b\xb6avj\x0b\x18\xcd\xb8\xb6=J\x190[\xa9b\r\xc1\r\x98v\xf3\xd7q\x13\xf3{W\xa2\x1b\xaa\x8b\xf2\xe6\xcf\xe8M|&\x86\x03\xe6Pfa\xea\x03'
PASSWORD_PATTERN = r'^(?=[^A-Z]*[A-Z])(?=[^a-z]*[a-z])(?=\D*\d)[\w\W]{8,}$'

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/sign-up")
@validate_request(SignUpBody)
async def sign_up(data: SignUpBody):
    username_pattern = r'^[a-zA-Z0-9_-]{3,32}$'
    if not re.fullmatch(username_pattern, data.username):
        return {"message": "Invalid username"}, 400

    if not re.fullmatch(PASSWORD_PATTERN, data.password):
        return {"message": "Invalid password"}, 400

    async with async_session() as session:
        statement = sa.select(User).where((User.email == data.email) | (User.username == data.username))
        result = await session.execute(statement)
        existing_user = result.scalars().first()

        if existing_user:
            return {"message": "User already exists"}, 409

        user = User(username=data.username, email=data.email,
                    password=pw_hash(data.password))  # hash password before sending over to database

        otp = await generate_otp()
        await create_otp(user.email, otp, user.password)
        send_otp_email(user.email, otp)

        otp_session["username"] = user.username
        otp_session["email"] = user.email
        return {"message": "Sign up completed, move to OTP"}, 200


@auth_bp.post("/otp")
@validate_request(OTPBody)
async def OTP(data: OTPBody):
    if otp_session.get("email") is None or otp_session.get("username") is None:
        return {"message": "Invalid request"}, 401

    email = otp_session.get("email")

    # Grab OTP and password from database
    otp = await get_otp(email)

    # Check if OTP is correct
    if otp.otp != data.otp:
        return {"message": "Invalid OTP"}, 401

    # Delete OTP from database
    # Create user
    username = otp_session.get("username")
    password = otp.password
    user = User(username, email, password)
    async with async_session() as session:
        async with session.begin():
            session.add(user)

    await delete_otp(email)
    await log_info(f"User {user.username} has been created using {user.email}")

    return {"message": "User successfully created"}, 200


@auth_bp.post("/login")
@validate_request(LoginBody)
async def login(data: LoginBody):
    invalid_cred_response = {"message": "Invalid credentials"}, 401

    device_id = str(uuid4())
    browser_data = BrowsingData(*await get_user_agent_data(request.user_agent.string),
                                await get_location_from_ip(request.remote_addr))

    # Check if user exists
    async with async_session() as session:
        account_check_statement = sa.select(User).where(
            (User.username == data.username) | (User.email == data.username)
        )
        existing_user: User = (await session.execute(account_check_statement)).scalars().first()

    if not existing_user:
        await log_info(
            f"Login using Username/email {data.username} has failed to login in using {browser_data.browser}, {browser_data.os} from {browser_data.location}"
        )
        return invalid_cred_response

    locked_out_user = await get_lockout(existing_user.user_id)

    if locked_out_user:
        if (datetime.datetime.now() - locked_out_user.lockout) < datetime.timedelta(minutes=5):
            await log_warning(
                f"User {existing_user.username} has failed to log in due to account lockout using {browser_data.browser}, {browser_data.os} from {browser_data.location}"
            )
            return invalid_cred_response

        await delete_lockout(locked_out_user.user_id)

    if pw_verify(existing_user.password, data.password):
        logged_in_user = existing_user
        await add_logged_in_device(session, device_id, logged_in_user.user_id, browser_data)
        # TODO(br1ght) re-enable when needed
        # await send_login_alert_email(logged_in_user, browser, os, location, request.remote_addr)
        login_user(AuthedUser(f"{logged_in_user.user_id}.{device_id}"))
        await log_info(f"User {logged_in_user.username} has logged in using {browser_data.browser}, {browser_data.os} from {browser_data.location}")
        return {"message": "login success"}, 200

    return await evaluate_failed_attempts(existing_user, invalid_cred_response, browser_data)


@auth_bp.post("/2fa")
async def two_fa():
    return {"message": "login success"}, 200


@auth_bp.post("/forgot-password")
@validate_request(ForgotPasswordBody)
async def forgot_password(data: ForgotPasswordBody):
    url_serialiser = current_app.config["url_serialiser"]
    email = data.email
    token = url_serialiser.dumps(email, FORGET_PASSWORD_SALT)
    send_password_recovery_email(email, token)
    return {"message": "Email Sent"}, 200


@auth_bp.post("/reset-password")
@validate_request(ResetPasswordBody)
async def reset_password(data: ResetPasswordBody):
    url_serialiser: URLSafeTimedSerializer = current_app.config["url_serialiser"]
    try:
        email = url_serialiser.loads(data.token, 3600, salt=FORGET_PASSWORD_SALT)
    except BadData:
        return {"message": "Invalid token"}, 401
    except SignatureExpired:
        return {"message": "Token expired"}, 401

    if not re.fullmatch(PASSWORD_PATTERN, data.password):
        return {"message": "Invalid password"}, 400

    # Password Hash
    hashed_password = pw_hash(data.password)

    # Replace password
    async with async_session() as session:
        update_statement = sa.update(User).where(User.email == email).values(password=hashed_password)
        await session.execute(update_statement)
        # Get user_id from email
        user_id = sa.select(User.user_id).where(User.email == email)
        # Remove any lockouts and failed attempts
        await delete_lockout(user_id)
        await delete_failed_attempt(user_id)
        await session.commit()
        return {"message": "Password reset"}, 200


@auth_bp.post("/login-callback")
@validate_request(LoginCallBackBody)
async def login_callback(data: LoginCallBackBody):
    device_id = str(uuid4())
    browser_data = BrowsingData(*await get_user_agent_data(request.user_agent.string),
                                await get_location_from_ip(request.remote_addr))

    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        id_info = id_token.verify_oauth2_token(data.token,
                                               requests.Request(),
                                               "758319541478-uflvh47eoagk6hl73ss1m2hnj35vk9bq.apps.googleusercontent.com",
                                               15)

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        user_id = id_info['sub']
        email = id_info['email']
        name = id_info['name']
        picture = id_info['picture']

        # Check if user exists in the database with the user_id provided
        async with async_session() as session:
            existing_user = await get_user_details(user_id)

            if existing_user is None:
                # Create a new user
                await insert_user_by_google(user_id, name, email, picture)
                await add_logged_in_device(session, device_id, user_id, browser_data)
                login_user(AuthedUser(f"{user_id}.{device_id}"))
                await log_info(f"User {name} has logged in using {browser_data.browser}, {browser_data.os} from {browser_data.location}")
                return {"message": "login success"}, 200

            await add_logged_in_device(session, device_id, user_id, browser_data)
            login_user(AuthedUser(f"{user_id}.{device_id}"))
            await log_info(f"User {name} has logged in using {browser_data.browser}, {browser_data.os} from {browser_data.location}")
            return {"message": "login success"}, 200
    except ValueError as err:
        # Invalid token
        print(err)
        return {"message": "Invalid token or something went wrong with the process"}, 401


@auth_bp.post("/logout")
@login_required
async def logout():
    try:
        await remove_logged_in_device(await current_user.device_id, await current_user.user_id)
        logout_user()
    except RuntimeError:
        return {"message": "Failed to logout"}, 500
    return {"message": "Successful logout"}, 200


@auth_bp.get("/is-logged-in")
@validate_response(UserData)
async def is_logged_in():
    if not await current_user.is_authenticated or not await current_user.user_id:
        return {"message": "Not authenticated"}, 401

    return UserData(await current_user.user_id,
                    await current_user.device_id,
                    await current_user.username,
                    await current_user.email,
                    await current_user.avatar,
                    await current_user.dark_mode,
                    await current_user.malware_scan,
                    await current_user.friends_only,
                    await current_user.censor)
