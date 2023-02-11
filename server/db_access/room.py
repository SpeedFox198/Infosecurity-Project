import sqlalchemy as sa
from db_access.globals import async_session
from models import Membership, Room, User
from sqlalchemy.orm.exc import NoResultFound


async def db_update_disappearing(disappearing: str, room_id: str):
    async with async_session() as session:
        statement = sa.update(Room).where(Room.room_id == room_id).values(disappearing=disappearing)
        await session.execute(statement)
        await session.commit()


async def db_get_room_if_user_verified(room_id: str, user_id: str) -> Room | None:
    async with async_session() as session:
        statement = sa.select(Room).join_from(Room, Membership).where(
            (Room.room_id == room_id) & (Membership.user_id == user_id)
        )

        try:
            async with session.begin():
                result = (await session.execute(statement)).one()
        except NoResultFound:
            return
        else:
            return result[0]


async def db_check_and_set_room_encrypted(user_id: str) -> list[str]:
    async with async_session() as session:
        subquery_statement = sa.select(
            Membership.room_id
        ).where(
            Membership.user_id == user_id
        ).subquery()

        statement = sa.select(
            Room.room_id, Membership.user_id
        ).join_from(
            Room, Membership
        ).where(
            (Room.type == "direct") &
            (Room.room_id.in_(sa.select(subquery_statement))) &
            (Membership.user_id != user_id)
        )

        result = (await session.execute(statement)).all()

        user_ids = [user_id for _, user_id in result]

        statement = sa.select(User.user_id).where(
            (User.user_id.in_(user_ids)) &
            (User.e2ee == True)
        )

        user_ids = (await session.execute(statement)).scalars().all()

        room_ids = [room_id for room_id, user_id in result if user_id in user_ids]

        statement = sa.update(Room).where(
            Room.room_id.in_(room_ids)
        ).values(encrypted=True)
        print("but why")

        await session.execute(statement)
        await session.commit()

    return room_ids
