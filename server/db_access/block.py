import sqlalchemy as sa
from sqlalchemy.orm.exc import NoResultFound
from db_access.globals import async_session
from models import Block, Membership


async def get_blocked(user_id: str) -> list[Block]:
    async with async_session() as session:

        # Retrieve blocked rooms
        statement = sa.select(Block).where(
            (Block.user_id == user_id) |
            (Block.block_id == user_id)
        )
        blocked = (await session.execute(statement)).scalars().all()

        # Return a list of blocked rooms
        return blocked


async def create_block_entry(user_id: str, block_id: str, room_id: str) -> bool:
    async with async_session() as session:
        # Retrieve room and membership info of user
        statement = sa.select(Membership.room_id).join_from(Membership).where(
            (Membership.room_id == room_id) &
            (
                (Membership.user_id == user_id) |
                (Membership.user_id == block_id)
            )
        )

        async with session.begin():
            try:
                (await session.execute(statement)).one()
            except NoResultFound:
                return False

            session.add(Block(user_id, block_id, room_id))

    return True
