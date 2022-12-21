import datetime
import re
from uuid import uuid4
from quart import Blueprint, request
from quart import session as otp_session
from security_functions.cryptography import *
from quart_auth import (
    login_user,
    logout_user,
    login_required,
    current_user
)
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
    OTPBody
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
    send_lockout_alert_email, send_login_alert_email
)

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")


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

        user = User(username=data.username, email=data.email, password=pw_hash(data.password)) # hash password before sending over to database

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
        existing_user = (await session.execute(account_check_statement)).scalars().first()

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

    async with async_session() as session:
        statement = sa.select(User).where(
            (
                (User.email == data.username) | (User.username == data.username)
            )
            & (User.password == pw_hash(data.password)) # comparing new hash with old hash
        )
        result = await session.execute(statement)
        logged_in_user = result.scalars().first()

    if logged_in_user:
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
