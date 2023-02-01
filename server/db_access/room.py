import sqlalchemy as sa
from db_access.globals import async_session
from models import Room, Membership
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
