from quart import Blueprint, request
from quart_auth import (
    login_user,
    logout_user,
    login_required,
    current_user
)
from quart_schema import validate_request

import sqlalchemy as sa

from .functions import (
    add_logged_in_device,
    get_location_from_ip,
    get_user_agent_data
)
from db_access.globals import async_session
from models import (
    User,
    AuthedUser,
    LoginData
)


auth_bp = Blueprint('auth', __name__, url_prefix="/auth")


@auth_bp.post("/login")
@validate_request(LoginData)
async def login(data: LoginData):
    async with async_session() as session:
        statement = sa.select(User).where((User.email == data.username) & (User.password == data.password))
        result = await session.execute(statement)
        user = result.scalars().first()

        if not user:
            return {"message": "invalid credentials"}, 401

        login_user(AuthedUser(user.user_id))
        location = await get_location_from_ip(request.remote_addr)
        browser, os = await get_user_agent_data(request.user_agent.string)

        return {"message": "login success"}, 200


@auth_bp.post("/logout")
@login_required
async def logout():
    logout_user()
    return {"message": "successful logout"}, 200


@auth_bp.get("/is-logged-in")
async def is_logged_in():
    if not await current_user.is_authenticated:
        return {"message": "not authenticated"}, 401

    return {
        "user_id": current_user.auth_id,
        "username": await current_user.username,
        "email": await current_user.email,
        "avatar": await current_user.avatar,
        "dark_mode": await current_user.dark_mode,
        "malware_scan": await current_user.malware_scan,
        "friends_only": await current_user.friends_only,
        "censor": await current_user.censor
    }
