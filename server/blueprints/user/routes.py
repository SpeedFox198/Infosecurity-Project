import sqlalchemy as sa
from db_access.globals import async_session
from models import User
from quart import Blueprint
from sqlalchemy.orm.exc import NoResultFound


user_bp = Blueprint("user", __name__, url_prefix="/user")


# TODO(medium)(SpeedFox198): validate_request, and also verify user is logged in
@user_bp.get("/details/<string:user_id>")
async def user_details(user_id: str):
    if not user_id:
        return {"message": "User does not exist."}, 404

    async with async_session() as session:
        statement = sa.select(User.username, User.avatar).where(User.user_id == user_id)
        try:
            user = (await session.execute(statement)).one()
        except NoResultFound:
            return {"message": "User does not exist."}, 404

    return {
        "username": user[0],
        "avatar": user[1]
    }
