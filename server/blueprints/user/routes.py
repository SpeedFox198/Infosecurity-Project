import sqlalchemy as sa
from db_access.globals import async_session
from models import User, Friend
from quart import Blueprint
from quart_auth import current_user, login_required
from sqlalchemy.orm.exc import NoResultFound

from models.response_data import FriendData

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


@user_bp.get("/friends")
@login_required
async def user_friends():
    current_user_id: str = await current_user.user_id

    async with async_session() as session:
        statement = sa.select(Friend).where(
            (Friend.user1_id == current_user_id) |
            (Friend.user2_id == current_user_id)
        )
        result: list[Friend] = (await session.execute(statement)).scalars().all()
        friend_user_id_list = [
            i.user1_id
            if i.user2_id == current_user_id
            else i.user2_id
            for i in result
        ]

        statement = sa.select(User.user_id, User.username, User.avatar).where(User.user_id.in_(friend_user_id_list))
        friend_list: list[tuple] = (await session.execute(statement)).all()

    return {"friends": [
        FriendData(*friend)
        for friend in friend_list
    ]}
