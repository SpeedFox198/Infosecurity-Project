from quart import Blueprint
from quart_auth import login_required, current_user
import sqlalchemy as sa
from quart_schema import validate_response

from db_access.globals import async_session
from models import Friend, User, FriendRequest
from models.response_data import FriendData, FriendRequestsData

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


@friend_bp.get("/requests")
@login_required
@validate_response(FriendRequestsData)
async def get_friend_requests():
    async with async_session() as session:
        recipient_statement_subquery = sa.select(FriendRequest.sender).where(
            FriendRequest.recipient == await current_user.user_id
        ).subquery()
        recipient_statement = sa.select(User.user_id, User.username, User.avatar).where(
            User.user_id.in_(sa.select(recipient_statement_subquery))
        )

        sender_statement_subquery = sa.select(FriendRequest.recipient).where(
            FriendRequest.sender == await current_user.user_id
        ).subquery()
        sender_statement = sa.select(User.user_id, User.username, User.avatar).where(
            User.user_id.in_(sa.select(sender_statement_subquery))
        )

        received_requests: list[tuple[str, str, str]] = (await session.execute(recipient_statement)).all()
        sent_requests: list[tuple[str, str, str]] = (await session.execute(sender_statement)).all()

    return FriendRequestsData(sent=[FriendData(*friend) for friend in sent_requests],
                              received=[FriendData(*friend) for friend in received_requests])