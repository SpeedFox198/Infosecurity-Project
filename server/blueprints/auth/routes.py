import datetime
from uuid import uuid4

from quart import Blueprint, request
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
from models.request_data import LoginBody
from models.response_data import UserData
from models.request_data import SignUpBody
from server.models import FailedAttempts, Lockout
from .functions import generate_otp, send_otp_email
from db_access.failed_attempts import get_failed_attempt, create_failed_attempt, update_failed_attempt, delete_failed_attempt
from db_access.account_lockout import get_lockout, create_lockout, delete_lockout

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")


@auth_bp.post("/sign-up")
@validate_request(SignUpBody)
async def sign_up(data: SignUpBody):
    async with async_session() as session:
        statement = sa.select(User).where((User.email == data.email) | (User.username == data.username))
        result = await session.execute(statement)
        existing_user = result.scalars().first()

        if existing_user:
            return {"message": "User already exists"}, 409

        user = User(username=data.username, email=data.email, password=data.password)
        session.add(user)
        await session.commit()
        otp = generate_otp()
        send_otp_email(user.email, otp)
        return {"message": "User created"}, 200


@auth_bp.post("/OTP")
async def OTP():
    return {"message": "sign up success"}, 200


@auth_bp.post("/login")
@validate_request(LoginBody)
async def login(data: LoginBody):
    async with async_session() as session:
        statement = sa.select(User).where((User.email == data.username) & (User.password == data.password))
        result = await session.execute(statement)
        user = result.scalars().first()
        if not user:
            #Check if user exists
            username_check = sa.select(User).where(User.email == data.username)
            if await session.execute(username_check) == True:
                
                #Check if a failed attempt exists
                if get_failed_attempt(data.username)[1] == False:
                    create_failed_attempt(data.username, 1)
                    return {"message": "invalid credentials"}, 401
                    
                #Update failed attempt if less than 5
                if get_failed_attempt(data.username)[1] < 5 and get_failed_attempt(data.username)[1] > 0:
                    update_failed_attempt(data.username, get_failed_attempt(data.username)[1] + 1)
                    return {"message": "invalid credentials"}, 401

                #Check if 5 failed attempts have been made
                if get_failed_attempt(data.username)[1] == 5:
                    create_lockout(data.username)
                    delete_failed_attempt(data.username)
                    return {"message": "invalid credentials"}, 401
            else:
                return {"message": "invalid credentials"}, 401
        #Check if account is locked
        if get_lockout(data.username)[1] is not None:
            #Check if lockout is less than 5 minutes
            if datetime.datetime.now() - get_lockout(data.username)[1] < datetime.timedelta(minutes=5):
                return {"message": "invalid credentials"}, 401
            else:
                delete_lockout(data.username)
                #Lock out timer expired

        device_id = str(uuid4())
        await add_logged_in_device(session, device_id, user.user_id, request)
        login_user(AuthedUser(f"{user.user_id}.{device_id}"))
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
