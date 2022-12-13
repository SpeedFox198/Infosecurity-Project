import datetime
import re
from uuid import uuid4
from quart_session import Session
from quart import Blueprint, request, session as otp_session 
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
from models.request_data import LoginBody, SignUpBody, OTPBody
from models.response_data import UserData

from .functions import generate_otp, send_otp_email
from db_access.failed_attempts import get_failed_attempt, create_failed_attempt, update_failed_attempt, delete_failed_attempt
from db_access.account_lockout import get_lockout, create_lockout, delete_lockout, get_email
from db_access.otp import get_otp, create_otp, delete_otp
from db_access.failed_attempts import get_failed_attempt, create_failed_attempt, update_failed_attempt, \
    delete_failed_attempt
from db_access.account_lockout import get_lockout, create_lockout, delete_lockout
from utils.logging import log_info
from .functions import generate_otp, send_otp_email, get_user_agent_data, get_location_from_ip, send_alert_email

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

        user = User(username=data.username, email=data.email, password=data.password)
        await log_info(f"User {user.username} has been created using {user.email}")
        otp = generate_otp()
        await create_otp(user.email, otp, user.password)
        send_otp_email(user.email, otp)
        otp_session["username"] = user.username
        otp_session["email"] = user.email
        await session.commit()
        return {"message": "User created"}, 200


@auth_bp.post("/OTP")
@validate_request(OTPBody)
async def OTP(data : OTPBody):
    email = otp_session.get("email")
    async with async_session() as session:
        #Grab OTP and password from database
        print(await get_otp(email))
        otp = (await get_otp(email))[1]
    #Check if OTP is correct
    if otp == data.otp:
        #Delete OTP from database
        #Create user
        username = otp_session.get("username")
        password = (await get_otp(email))[2]
        user = User(username, email, password)
        session.add(user)
        await delete_otp(email)
        await session.commit()
        return {"message": "sign up success"}, 200
    else:
        return {"message": "invalid OTP"}, 401


@auth_bp.post("/login")
@validate_request(LoginBody)
async def login(data: LoginBody):
    device_id = str(uuid4())
    browser, os = await get_user_agent_data(request.user_agent.string)
    location = await get_location_from_ip(request.remote_addr)

    async with async_session() as session:
        statement = sa.select(User).where(
            (
                (User.email == data.username) | (User.username == data.username)
            )
            & (User.password == data.password)
        )
        result = await session.execute(statement)
        user = result.scalars().first()
        if not user:
            # Check if user exists
            username_check = sa.select(User).where(User.email == data.username)
            if (await session.execute(username_check)) == True:

                # Check if a failed attempt exists
                if (await get_failed_attempt(data.username))[1] == False:
                    await create_failed_attempt(data.username, 1)
                    await log_info(f"User {data.username} has failed to log in using {browser}, {os} from {location}")
                    return {"message": "invalid credentials"}, 401

                # Update failed attempt if less than 5
                if (await get_failed_attempt(data.username))[1] < 5 and (await get_failed_attempt(data.username))[
                    1] > 0:
                    await update_failed_attempt(data.username, await get_failed_attempt(data.username)[1] + 1)
                    await log_info(f"User {data.username} has failed to log in using {browser}, {os} from {location}")
                    return {"message": "invalid credentials"}, 401

                # Check if 5 failed attempts have been made
                if (await get_failed_attempt(data.username))[1] == 5:
                    await create_lockout(data.username)
                    await delete_failed_attempt(data.username)

                    #Grab email
                    email = (await get_email(data.username))[1]

                    #Send alert email
                    send_alert_email(email)
                    
                    await log_info(f"User {data.username} has failed to log in using {browser}, {os} from {location}")
                    return {"message": "invalid credentials"}, 401

            else:
                await log_info(f"User {data.username} has failed to log in using {browser}, {os} from {location}")
                return {"message": "invalid credentials"}, 401
        # Check if account is locked
        if (await get_lockout(data.username)) == True:
            # Check if lockout is less than 5 minutes
            if datetime.datetime.now() - (await get_lockout(data.username))[1] < datetime.timedelta(minutes=5):
                return {"message": "invalid credentials"}, 401
            else:
                await delete_lockout(data.username)
                # Lock out timer expired
            return {"message": "invalid credentials"}, 401

        await add_logged_in_device(session, device_id, user.user_id, browser, os, location)
        login_user(AuthedUser(f"{user.user_id}.{device_id}"))
        await log_info(f"User {user.username} has logged in using {browser}, {os} from {location}")
        return {"message": "login success"}, 200


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
