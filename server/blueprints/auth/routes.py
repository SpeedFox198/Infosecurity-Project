import datetime
import re
from urllib.parse import urlparse, parse_qs
from uuid import uuid4
import pyotp

import sqlalchemy as sa
from google.auth.transport import requests
from google.oauth2 import id_token
from itsdangerous import BadData, SignatureExpired, URLSafeTimedSerializer
from quart import Blueprint, current_app, request
from quart import session as auth_session
from quart_auth import current_user, login_required, login_user, logout_user
from quart_schema import validate_request, validate_response

from db_access.account_lockout import delete_lockout, get_lockout
from db_access.device import add_logged_in_device, remove_logged_in_device
from db_access.failed_attempt import delete_failed_attempt
from db_access.globals import async_session
from db_access.otp import create_otp, delete_otp, get_otp
from db_access.user import get_user_details, insert_user_by_google, reset_password_with_email, get_user_id
from google_authenticator import get_google_oauth_flow
from models import AuthedUser, User
from models.general.BrowsingData import BrowsingData
from models.request_data import (
    ForgotPasswordBody,
    LoginBody,
    OTPBody,
    ResetPasswordBody,
    SignUpBody,
    GoogleCallBackBody,
    BackupCodeBody
)
from models.response_data import UserData
from security_functions.cryptography import pw_hash, pw_verify
from db_access.twoFA import get_2fa
from models.request_data import TwoFABody
from db_access.backup_codes import get_2fa_backup_codes, delete_2fa_backup_codes
from utils.logging import log_info, log_warning, log_exception
from .functions import (
    generate_otp,
    get_location_from_ip,
    get_user_agent_data,
    send_otp_email,
    send_password_recovery_email,
    evaluate_failed_attempts,
    send_login_alert_email
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

        auth_session["otp_username"] = user.username
        auth_session["otp_email"] = user.email
        await log_info(f"User {user.username} has signed up.")
        return {"message": "Sign up completed, move to OTP"}, 200


@auth_bp.post("/otp")
@validate_request(OTPBody)
async def OTP(data: OTPBody):
    if auth_session.get("otp_email") is None or auth_session.get("otp_username") is None:
        return {"message": "Invalid request"}, 401

    email = auth_session.get("otp_email")

    # Grab OTP and password from database
    otp = await get_otp(email)

    # Check if OTP is correct
    if otp.otp != data.otp:
        return {"message": "Invalid OTP"}, 401

    # Delete OTP from database
    # Create user
    username = auth_session.get("otp_username")
    password = otp.password
    user = User(username, email, password)
    async with async_session() as session:
        async with session.begin():
            session.add(user)

    await delete_otp(email)
    await log_info(f"User {user.username} has been created")

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
            f"Login with {data.username} has failed to login in using {browser_data.browser}, {browser_data.os} from {browser_data.location}"
        )
        return invalid_cred_response

    locked_out_user = await get_lockout(existing_user.user_id)

    if locked_out_user:
        if (datetime.datetime.now() - locked_out_user.lockout) < datetime.timedelta(minutes=30):
            await log_warning(
                f"User {existing_user.username} has failed to log in due to account lockout using {browser_data.browser}, {browser_data.os} from {browser_data.location}"
            )
            return invalid_cred_response

        await delete_lockout(existing_user.user_id)

    if not pw_verify(existing_user.password, data.password):
        return await evaluate_failed_attempts(existing_user, invalid_cred_response, browser_data)

    # Check if user has 2FA enabled
    if await get_2fa_backup_codes(existing_user.user_id):
        auth_session["login_existing_user"] = existing_user.user_id
        return {"message": "2FA required"}, 200

    logged_in_user = existing_user
    await add_logged_in_device(session, device_id, logged_in_user.user_id, browser_data)
    await send_login_alert_email(logged_in_user, browser_data, request.remote_addr)
    login_user(AuthedUser(f"{logged_in_user.user_id}.{device_id}"))
    await log_info(
        f"User {logged_in_user.username} has logged in using {browser_data.browser}, {browser_data.os} from {browser_data.location}")
    return {"message": "login success"}, 200


@auth_bp.post("/2fa")
@validate_request(TwoFABody)
async def two_fa(data: TwoFABody):
    user_id = auth_session.get("login_existing_user")

    if auth_session.get("login_existing_user") is None:
        return {"message": "Invalid request"}, 401

    async with async_session() as session:
        existing_user: User = (await session.execute(sa.select(User).where(User.user_id == user_id))).scalars().first()

    device_id = str(uuid4())
    browser_data = BrowsingData(*await get_user_agent_data(request.user_agent.string),
                                await get_location_from_ip(request.remote_addr))
    twoFA_code = await get_2fa(user_id)
    secret_token = twoFA_code.secret
    OTP_check = data.twofacode
    verified = pyotp.TOTP(secret_token).verify(OTP_check)

    if verified:
        logged_in_user = existing_user
        await add_logged_in_device(session, device_id, logged_in_user.user_id, browser_data)
        await send_login_alert_email(logged_in_user, browser_data, request.remote_addr)
        login_user(AuthedUser(f"{logged_in_user.user_id}.{device_id}"))
        await log_info(
            f"User {logged_in_user.username} has logged in using {browser_data.browser}, {browser_data.os} from {browser_data.location}"
        )
        return {"message": "login success"}, 200
    else:
        await log_info(
            f"User {existing_user.username} has failed to login with 2fa using {browser_data.browser}, {browser_data.os} from {browser_data.location}"
        )
        return {"message": "Invalid 2FA code"}, 400


@auth_bp.post("/backupcode")
@validate_request(BackupCodeBody)
async def backupcode(data: BackupCodeBody):
    user_id = auth_session.get("login_existing_user")
    device_id = str(uuid4())
    browser_data = BrowsingData(*await get_user_agent_data(request.user_agent.string),
                                await get_location_from_ip(request.remote_addr))
    async with async_session() as session:
        existing_user: User = (await session.execute(sa.select(User).where(User.user_id == user_id))).scalars().first()
    backup_code: list[str] = [
        bc.code
        for bc in await get_2fa_backup_codes(existing_user.user_id)
    ]
    for i in backup_code:
        if data.backupcode == i:
            # If the backup code is in the list, delete the backup code from the list
            await delete_2fa_backup_codes(existing_user.user_id, data.backupcode)
            logged_in_user = existing_user
            await add_logged_in_device(session, device_id, logged_in_user.user_id, browser_data)
            await send_login_alert_email(logged_in_user, browser_data, request.remote_addr)
            login_user(AuthedUser(f"{logged_in_user.user_id}.{device_id}"))
            await log_info(
                f"User {logged_in_user.username} has logged in using {browser_data.browser}, {browser_data.os} from {browser_data.location}")
            return {"message": "login success"}, 200

    await log_info(
        f"User {existing_user.username} has failed to log in with invalid backup code using {browser_data.browser}, {browser_data.os} from {browser_data.location}"
    )
    return {"message": "Invalid backup code"}, 400


@auth_bp.post("/forgot-password")
@validate_request(ForgotPasswordBody)
async def forgot_password(data: ForgotPasswordBody):
    browser_data = BrowsingData(*await get_user_agent_data(request.user_agent.string),
                                await get_location_from_ip(request.remote_addr))
    if get_user_id(data.email) is None:
        await log_info(
            f"Invalid forgot password request of {data.email} using {browser_data.browser}, {browser_data.os} from {browser_data.location}"
        )
        return {"message": "Email sent"}, 200

    url_serialiser = current_app.config["url_serialiser"]
    email = data.email
    token = url_serialiser.dumps(email, FORGET_PASSWORD_SALT)
    send_password_recovery_email(email, token)
    await log_info(
        f"Forgot password request of {data.email} sent using {browser_data.browser}, {browser_data.os} from {browser_data.location}"
    )
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
    await reset_password_with_email(email, hashed_password)
    user_id = await get_user_id(email)
    await delete_lockout(user_id)
    await delete_failed_attempt(user_id)
    await log_info(
        f"User {user_id}'s password has been reset"
    )
    return {"message": "Password reset"}, 200


@auth_bp.post("/google-callback")
@validate_request(GoogleCallBackBody)
async def google_callback(data: GoogleCallBackBody):
    device_id = str(uuid4())
    browser_data = BrowsingData(*await get_user_agent_data(request.user_agent.string),
                                await get_location_from_ip(request.remote_addr))

    google_flow = get_google_oauth_flow()
    google_state = auth_session.get("google_state")
    authorization_response = request.url + data.parameters

    state_from_parameters = parse_qs(urlparse(authorization_response).query)["state"][0]

    try:
        google_flow.fetch_token(authorization_response=authorization_response)
    except Exception as err:
        await log_exception(err)
        await log_info(
            f"Invalid Google login using {browser_data.browser}, {browser_data.os} from {browser_data.location}"
        )
        return {"message": "Error occurred while login with Google"}, 404

    if google_state != state_from_parameters:
        await log_info(
            f"Invalid Google login using {browser_data.browser}, {browser_data.os} from {browser_data.location}"
        )
        return {"message": "Invalid Google Login"}, 401

    credentials = google_flow.credentials

    try:
        id_info = id_token.verify_oauth2_token(credentials.id_token,
                                               requests.Request(),
                                               "758319541478-uflvh47eoagk6hl73ss1m2hnj35vk9bq.apps.googleusercontent.com",
                                               15)
    except ValueError as err:
        await log_exception(err)
        await log_info(
            f"Invalid Google login using {browser_data.browser}, {browser_data.os} from {browser_data.location}"
        )
        return {"message": "Invalid token or something went wrong with the process"}, 401

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
    await log_info(
        f"User {name} has logged in using {browser_data.browser}, {browser_data.os} from {browser_data.location}"
    )
    return {"message": "login success"}, 200


@auth_bp.get("/google-login")
async def google_login():
    authorisation_url, state = get_google_oauth_flow().authorization_url(
        access_type="offline",
        include_granted_scopes="true"
    )

    auth_session["google_state"] = state
    return {"google_auth_url": authorisation_url}, 200


@auth_bp.post("/logout")
@login_required
async def logout():
    try:
        await remove_logged_in_device(await current_user.device_id, await current_user.user_id)
        logout_user()
    except RuntimeError as err:
        await log_exception(err)
        return {"message": "Failed to logout"}, 500

    return {"message": "Successful logout"}, 200


@auth_bp.get("/is-logged-in")
@validate_response(UserData)
async def is_logged_in():
    if not await current_user.is_authenticated or not await current_user.user_id:
        return {"message": "Not authenticated"}, 401

    return UserData(
        await current_user.user_id,
        await current_user.device_id,
        await current_user.username,
        await current_user.email,
        await current_user.avatar,
        await current_user.e2ee,
        await current_user.public_key,
        await current_user.dark_mode,
        await current_user.malware_scan,
        await current_user.friends_only,
        await current_user.censor,
        await current_user.google_account
    )
