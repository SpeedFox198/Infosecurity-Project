from quart import Blueprint, request
from quart_auth import (
    login_user,
    logout_user,
    login_required,
    current_user
)
from quart_schema import validate_request

import sqlalchemy as sa

from db_access.globals import async_session
from models import (
    User,
    AuthedUser,
)


user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.get("/<string:user_id>")
async def user_details(user_id):

    if not user_id:
        return {"message": "User does not exist."}, 404

    user = None

    async with async_session() as session:
        statement = sa.select(User.username, User.avatar).where(User.user_id == user_id)
        # TODO(low)(SpeedFox198): handle error if more than one result is returned (read sqlalchemy docs)
        user = (await session.execute(statement)).one()

    if not user:
        return {"message": "User does not exist."}, 404

    return {
        "username": user[0],
        "avatar": user[1]
    }
