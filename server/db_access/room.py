import sqlalchemy as sa
from db_access.globals import async_session
from models import Room


async def db_update_disappearing(disappearing: str, room_id: str):
    async with async_session() as session:
        statement = sa.update(Room).where(Room.room_id == room_id).values(disappearing=disappearing)
        await session.execute(statement)
        await session.commit()
