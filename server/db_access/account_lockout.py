from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError

from db_access.globals import async_session
from models import Lockout
from models.User import User
from utils.logging import log_exception


# Create lockout
async def create_lockout(user_id: str) -> None:
    async with async_session() as session:
        statement = sa.insert(Lockout).values(user_id=user_id, lockout=datetime.now())
        try:
            await session.execute(statement)
            await session.commit()
        except SQLAlchemyError as err:
            await session.rollback()
            await log_exception(err)


# Retrieve lockout
async def get_lockout(user_id: str) -> Lockout | None:
    async with async_session() as session:
        statement = sa.select(Lockout).where(Lockout.user_id == user_id)
        result = await session.execute(statement)
        lockout = result.scalars().first()
        if lockout:
            return lockout


# Delete lockout by user_id
async def delete_lockout(user_id: str) -> None:
    async with async_session() as session:
        statement = sa.delete(Lockout).where(Lockout.user_id == user_id)
        try:
            await session.execute(statement)
            await session.commit()
        except SQLAlchemyError as err:
            await session.rollback()
            await log_exception(err)


# Get email from username
async def get_email(user_id: str) -> str | None:
    async with async_session() as session:
        statement = sa.select(User.email).where(User.user_id == user_id)
        result = await session.execute(statement)
        return result.scalar()
