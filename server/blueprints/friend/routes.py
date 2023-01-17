from quart import Blueprint
from quart_auth import login_required, current_user
import sqlalchemy as sa

from db_access.globals import async_session
from models import Friend, User
from models.response_data import FriendData

friend_bp = Blueprint("friends", __name__, url_prefix="/friends")


@friend_bp.get("/")
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


@friend_bp.post("/")
@login_required
async def create_friend_request():
    return {"message": "ball"}
