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

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")


@auth_bp.post("/sign-up")
@validate_request(SignUpBody)
async def sign_up(data: SignUpBody):
    async with async_session() as session:
        statement = sa.select(User).where((User.email == data.username) & (User.password == data.password))
        result = await session.execute(statement)
        user = result.scalars().first()
        if user:
            return {"message": "user already exists"}, 409
        user = User(email=data.username, password=data.password)
        session.add(user)
        await session.commit()
        device_id = str(uuid4())
        await add_logged_in_device(session, device_id, user.user_id, request)
        login_user(AuthedUser(f"{user.user_id}.{device_id}"))
        return {"message": "sign up success"}, 200


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
            return {"message": "invalid credentials"}, 401

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
