import sqlalchemy as sa
from db_access.globals import async_session
from models import Block, Membership, Room
from sqlalchemy.orm.exc import NoResultFound


async def db_get_blocked(user_id: str) -> list[Block]:
    async with async_session() as session:

        # Retrieve blocked rooms
        statement = sa.select(Block).where(
            (Block.user_id == user_id) |
            (Block.block_id == user_id)
        )
        blocked = (await session.execute(statement)).scalars().all()

        # Return a list of blocked rooms
        return blocked


async def db_create_block_entry(user_id: str, block_id: str, room_id: str) -> bool:
    async with async_session() as session:
        block_verify_statement = sa.select(Block).where((Block.room_id == room_id))
        membership_verify_statement = sa.select(Membership.room_id).where(
            (Membership.room_id == room_id) &
            (
                (Membership.user_id == user_id) |
                (Membership.user_id == block_id)
            )
        )

        room_verify_statement = sa.select(Room.type).where(Room.room_id == room_id)

        async with session.begin():
            entries = (await session.execute(block_verify_statement)).all()
            if entries:
                return False

            entries = (await session.execute(membership_verify_statement)).scalars().all()
            if len(entries) != 2:
                return False

            try:
                room_type = (await session.execute(room_verify_statement)).one()
            except NoResultFound:
                return False

            if room_type[0] != "direct":
                return False

            session.add(Block(user_id, block_id, room_id))

    return True


async def db_delete_block_entry(user_id: str, block_id: str, room_id: str) -> bool:
    async with async_session() as session:
        verify_statement = sa.select(Block).where(
            (Block.user_id == user_id) &
            (Block.block_id == block_id) &
            (Block.room_id == room_id)
        )

        delete_statement = sa.delete(Block).where(
            (Block.user_id == user_id) &
            (Block.block_id == block_id) &
            (Block.room_id == room_id)
        )

        async with session.begin():
            try:
                (await session.execute(verify_statement)).one()
            except NoResultFound:
                return False

            await session.execute(delete_statement)

    return True

async def db_check_block(room_id: str) -> Block | None:
    async with async_session() as session:

        statement = sa.select(Block).where(Block.room_id == room_id)
        blocked_room = (await session.execute(statement)).scalar()

        return blocked_room
