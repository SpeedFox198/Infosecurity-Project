import sqlalchemy as sa

from db_access.globals import async_session
from server.models import FailedAttempts

#Create failed login attempt
async def create_failed_attempt(user_id, attempt_no):
    async with async_session() as session:
        statement = sa.insert(FailedAttempts).values(user_id=user_id, attempts=attempt_no)
        try:
            await session.execute(statement)
            await session.commit()
        except:
            return False

#Update failed login attempt
async def update_failed_attempt(user_id, attempt_no):
    async with async_session() as session:
        statement = sa.update(FailedAttempts).where(FailedAttempts.user_id == user_id).values(attempts=attempt_no)
        try:
            await session.execute(statement)
            await session.commit()
        except:
            return False

#Retrieve failed login attempt
async def get_failed_attempt(user_id):
    async with async_session() as session:
        statement = sa.select(FailedAttempts).where(FailedAttempts.user_id == user_id)
        result = await session.execute(statement)
        failed_attempt = result.scalars().first()
        if failed_attempt:
            return failed_attempt
        return False

#Delete failed login attempt
async def delete_failed_attempt(user_id):
    async with async_session() as session:
        statement = sa.delete(FailedAttempts).where(FailedAttempts.user_id == user_id)
        try:
            await session.execute(statement)
            await session.commit()
        except:
            return False