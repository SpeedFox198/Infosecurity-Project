from sqlalchemy.exc import SQLAlchemyError

from db_access.globals import async_session
import sqlalchemy as sa

from models import User, SioConnection


async def set_online_status(user_id: str, status: bool) -> None:
    async with async_session() as session:
        try:
            statement = sa.update(User).where(User.user_id == user_id).values(online=status)
            await session.execute(statement)
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()


async def add_sio_connection(sid, user_id: str) -> None:
    async with async_session() as session:
        connection_exists_statement = sa.select(SioConnection).where(
            (SioConnection.sid == sid) &
            (SioConnection.user_id == user_id)
        )
        connection_exists = (await session.execute(connection_exists_statement)).scalar()
        if not connection_exists:
            session.add(SioConnection(sid, user_id))
            await session.commit()
            return

        check_diff_sid_statement = sa.select(SioConnection).where(
            (SioConnection.sid != sid) &
            (SioConnection.user_id == user_id)
        )
        diff_sid_connection: SioConnection | None = (await session.execute(check_diff_sid_statement)).scalar()

        if diff_sid_connection:
            try:
                update_sid_statement = sa.update(SioConnection)\
                    .where(SioConnection.sid == diff_sid_connection.sid)\
                    .values(sid=sid)
                await session.execute(update_sid_statement)
                await session.commit()
                await session.commit()
            except SQLAlchemyError:
                await session.rollback()


async def remove_sio_connection(sid, user_id: str) -> None:
    async with async_session() as session:
        try:
            statement = sa.delete(SioConnection).where(
                (SioConnection.sid == sid) & (SioConnection.user_id == user_id)
            )
            await session.execute(statement)
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()


async def get_sid_from_sio_connection(user_id: str):
    async with async_session() as session:
        statement = sa.select(SioConnection.sid).where(SioConnection.user_id == user_id)
        result = (await session.execute(statement)).scalar()
        return result
