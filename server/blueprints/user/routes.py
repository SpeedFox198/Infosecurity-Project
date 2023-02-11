import sqlalchemy as sa
from db_access.globals import async_session
from models import Membership, User
from models.request_data import SearchUserBody
from quart import Blueprint
from quart_schema import validate_request
from quart_auth import login_required
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


@user_bp.post("/find")
@validate_request(SearchUserBody)
async def find_user(data: SearchUserBody):
    async with async_session() as session:
        statement = sa.select(User.user_id, User.username, User.avatar).where(User.username.like(f"{data.username}%"))
        results = (await session.execute(statement)).all()
    return {"user_search_results": [
        {
            "user_id": user[0],
            "username": user[1],
            "avatar": user[2]
        }
        for user in results
        ]
    }


@user_bp.get("/public-key/<string:room_id>/<string:user_id>")
async def user_public_key(room_id: str, user_id: str):
    if not room_id or not user_id:
        return {"message": "Public key not found."}, 404

    async with async_session() as session:
        # Currently only supports direct messages
        statement = sa.select(User.public_key).where(
            User.user_id == sa.select(Membership.user_id).where(
                (Membership.room_id == room_id) &
                (Membership.user_id != user_id)
            ).scalar_subquery()
        )
        try:
            user = (await session.execute(statement)).one()
        except NoResultFound:
            return {"message": "Public key not found."}, 404

    return {
        "public_key": user[0]
    }


@user_bp.get("/wrap-key/<string:user_id>")
@login_required
async def user_wrap_key(user_id: str):
    if not user_id:
        return {"message": "User not found."}, 404

    async with async_session() as session:
        # Currently only supports direct messages
        statement = sa.select(User.wrap_key).where(
            User.user_id == user_id
        )
        try:
            wrap_key = (await session.execute(statement)).scalar()
        except NoResultFound:
            return {"message": "User not found."}, 404

    return {"wrap_key": wrap_key}
