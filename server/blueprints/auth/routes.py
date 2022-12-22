import datetime
import re
from uuid import uuid4
from quart import Blueprint, Quart, request
from quart import session as otp_session
from security_functions.cryptography import pw_hash, pw_verify
from quart_auth import (
    login_user,
    logout_user,
    login_required,
    current_user
)
from quart_cors import cors
from quart_schema import validate_request, validate_response

import sqlalchemy as sa

from db_access.device import remove_logged_in_device, add_logged_in_device
from db_access.globals import async_session
from models import (
    User,
    AuthedUser,
)
from models.request_data import (
    LoginBody,
    SignUpBody,
    OTPBody,
    LoginCallBackBody,
    ForgotPasswordBody,
    ResetPasswordBody
)
from models.response_data import UserData

from db_access.otp import get_otp, create_otp, delete_otp
from db_access.failed_attempt import (
    get_failed_attempt,
    create_failed_attempt,
    update_failed_attempt,
    delete_failed_attempt
)
from db_access.account_lockout import (
    get_lockout,
    create_lockout,
    delete_lockout,
    get_email
)
from utils.logging import log_info, log_warning
from .functions import (
    generate_otp,
    send_otp_email,
    get_user_agent_data,
    get_location_from_ip,
    send_lockout_alert_email, send_login_alert_email, send_password_recovery_email
)

saltkey = b'\x80\x1c\rqn\xb2\x7f\x03\x90\xeeA\x18ex\x0e\xc1\x14\xf7\xf3A\x8b\xbc\\]\x1ag\xd8\xcbk\xd3\x9a\x9a3\xce\x14\xbe\xc7\x1ak^K>\xb5jyu,:\xdaF\xc2\x08\xae5\xcf$\x90M[\xcd&\xc1\x90\x06\xa5i\x81\xfd70\xd3\x1d\x03\x06\xf4(Up6\x08b\xb6avj\x0b\x18\xcd\xb8\xb6=J\x190[\xa9b\r\xc1\r\x98v\xf3\xd7q\x13\xf3{W\xa2\x1b\xaa\x8b\xf2\xe6\xcf\xe8M|&\x86\x03\xe6Pfa\xea\x03'

from utils.app_context import AppContext

from google.oauth2 import id_token
from google.auth.transport import requests

from itsdangerous import SignatureExpired, URLSafeTimedSerializer, BadData

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")

auth_app_context = AppContext()

url_serialiser = URLSafeTimedSerializer(auth_app_context.secret_key)

@auth_bp.post("/sign-up")
@validate_request(SignUpBody)
async def sign_up(data: SignUpBody):
    username_regex = r'^[a-zA-Z0-9_-]{3,32}$'
    if not re.fullmatch(username_regex, data.username):
        return {"message": "Invalid username"}, 400

    async with async_session() as session:
        statement = sa.select(User).where((User.email == data.email) | (User.username == data.username))
        result = await session.execute(statement)
        existing_user = result.scalars().first()

        if existing_user:
            return {"message": "User already exists"}, 409

        user = User(username=data.username, email=data.email, password=pw_hash(data.password))  # hash password before sending over to database

        otp = generate_otp()
        await create_otp(user.email, otp, user.password)
        send_otp_email(user.email, otp)

        otp_session["username"] = user.username
        otp_session["email"] = user.email
        return {"message": "Sign up completed, move to OTP"}, 200


@auth_bp.post("/otp")
@validate_request(OTPBody)
async def OTP(data: OTPBody):
    email = otp_session.get("email")

    # Grab OTP and password from database
    otp = await get_otp(email)

    # Check if OTP is correct
    if otp.otp != data.otp:
        return {"message": "invalid OTP"}, 401

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
    browser, os = await get_user_agent_data(request.user_agent.string)
    location = await get_location_from_ip(request.remote_addr)

    # Check if user exists
    async with async_session() as session:
        account_check_statement = sa.select(User).where(
            (User.username == data.username) | (User.email == data.username)
        )
        existing_user: User = (await session.execute(account_check_statement)).scalars().first()

    if not existing_user:
        await log_info(
            f"Login using Username/email {data.username} has failed to login in using {browser}, {os} from {location}"
        )
        return invalid_cred_response

    locked_out_user = await get_lockout(existing_user.user_id)

    if locked_out_user:
        if (datetime.datetime.now() - locked_out_user.lockout) < datetime.timedelta(minutes=5):
            await log_warning(
                f"User {existing_user.username} has failed to log in due to account lockout using {browser}, {os} from {location}"
            )
            return invalid_cred_response

        await delete_lockout(locked_out_user.user_id)

    if pw_verify(existing_user.password, data.password):
        logged_in_user = existing_user
        await add_logged_in_device(session, device_id, logged_in_user.user_id, browser, os, location)
        # TODO(br1ght) re-enable when needed
        # await send_login_alert_email(logged_in_user, browser, os, location, request.remote_addr)
        login_user(AuthedUser(f"{logged_in_user.user_id}.{device_id}"))
        await log_info(f"User {logged_in_user.username} has logged in using {browser}, {os} from {location}")
        return {"message": "login success"}, 200

    failed_attempt = (await get_failed_attempt(existing_user.user_id))

    # Check if a failed attempt exists
    if failed_attempt is None:
        await create_failed_attempt(existing_user.user_id)
        await log_info(f"User {existing_user.username} has failed to log in using {browser}, {os} from {location}")
        return invalid_cred_response

    if 5 > failed_attempt.attempts > 0:
        await update_failed_attempt(failed_attempt.user_id, (failed_attempt.attempts + 1))
        await log_info(f"User {existing_user.username} has failed to log in using {browser}, {os} from {location}")
        return invalid_cred_response

    if failed_attempt.attempts == 5:
        await create_lockout(failed_attempt.user_id)
        await delete_failed_attempt(failed_attempt.user_id)

        lockout_user_email = await get_email(failed_attempt.user_id)
        send_lockout_alert_email(lockout_user_email)

        await log_warning(f"User {existing_user.username} has been locked out for 5 minutes.")
        return invalid_cred_response


@auth_bp.post("/2fa")
async def two_fa():
    return {"message": "login success"}, 200


@auth_bp.post("/forgot-password")
@validate_request(ForgotPasswordBody)
async def forgot_password(data : ForgotPasswordBody):
    email = data.email
    token = url_serialiser.dumps(email, saltkey)
    send_password_recovery_email(email, token)
    return {"message": "Email Sent"}, 200


@auth_bp.post("/reset-password")
@validate_request(ResetPasswordBody)
async def reset_password(data : ResetPasswordBody):
    try:
        email = url_serialiser.loads(data.token, saltkey, max_age=3600)
    except SignatureExpired:
        return {"message": "Token has expired"}, 401


@auth_bp.post("/login-callback")
@validate_request(LoginCallBackBody)
async def login_callback(data: LoginCallBackBody):
    csrf_token_cookie = request.cookies.get('g_csrf_token')
    if not csrf_token_cookie:
        return {"message": "No CSRF token in Cookie"}, 401
    csrf_token_body = request.get('g_csrf_token')
    if not csrf_token_body:
        return {"message": "No CSRF roken in post body"}, 401
    if csrf_token_cookie != csrf_token_body:
        return {"message": "Failed to verify double submit cookie"}, 401

    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(data.token, requests.Request(), "758319541478-uflvh47eoagk6hl73ss1m2hnj35vk9bq.apps.googleusercontent.com")

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
        email = idinfo['email']
        name = idinfo['name']
        picture = idinfo['picture']
        #Check if user exists in the database
        async with async_session() as session:
            statement = sa.select(User).where(User.email == email)
            result = await session.execute(statement)
            existing_user = result.scalars().first()
            if existing_user is None:
                await create_user(session, email, name, picture)
                statement = sa.select(User).where(User.email == email)
                result = await session.execute(statement)
                existing_user = result.scalars().first()


        
    except ValueError:
        # Invalid token
        return {"message": "Invalid token or something went wrong with the process"}, 401

    return {"message": "login success"}, 200

@auth_bp.post("/logout")
@login_required
async def logout():
    await remove_logged_in_device(current_user.device_id, current_user.user_id)
    logout_user()
    return {"message": "successful logout"}, 200


@auth_bp.get("/is-logged-in")
@validate_response(UserData)
async def is_logged_in():
    if not await current_user.is_authenticated or not await current_user.user_id:
        return {"message": "not authenticated"}, 401

    return UserData(await current_user.user_id,
                    await current_user.device_id,
                    await current_user.username,
                    await current_user.email,
                    await current_user.avatar,
                    await current_user.dark_mode,
                    await current_user.malware_scan,
                    await current_user.friends_only,
                    await current_user.censor)
