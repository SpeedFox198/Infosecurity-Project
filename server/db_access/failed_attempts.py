import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError

from db_access.globals import async_session
from models import FailedAttempts
from utils.logging import log_exception


# Create failed login attempt
async def create_failed_attempt(user_id: str) -> None:
    async with async_session() as session:
        statement = sa.insert(FailedAttempts).values(user_id=user_id, attempts=1)
        try:
            await session.execute(statement)
            await session.commit()
        except SQLAlchemyError as err:
            await session.rollback()
            await log_exception(err)


# Update failed login attempt
async def update_failed_attempt(user_id: str, attempt_no: int) -> None:
    async with async_session() as session:
        statement = sa.update(FailedAttempts).where(FailedAttempts.user_id == user_id).values(attempts=attempt_no)
        try:
            await session.execute(statement)
            await session.commit()
        except SQLAlchemyError as err:
            await session.rollback()
            await log_exception(err)


# Retrieve failed login attempt
async def get_failed_attempt(user_id: str) -> FailedAttempts | None:
    async with async_session() as session:
        statement = sa.select(FailedAttempts).where(FailedAttempts.user_id == user_id)
        result = await session.execute(statement)
        failed_attempt = result.scalars().first()
        if failed_attempt:
            return failed_attempt


# Delete failed login attempt
async def delete_failed_attempts(user_id: str) -> None:
    async with async_session() as session:
        statement = sa.delete(FailedAttempts).where(FailedAttempts.user_id == user_id)
        try:
            await session.execute(statement)
            await session.commit()
        except SQLAlchemyError as err:
            await session.rollback()
            await log_exception(err)
