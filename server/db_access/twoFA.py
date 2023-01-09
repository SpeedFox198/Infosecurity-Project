import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError

import models
from db_access.globals import async_session
from models import TwoFA
from utils.logging import log_exception

#Create 2FA
async def create_2fa(user_id, secret) -> None:
    async with async_session() as session:
        statement = sa.insert(models.TwoFA).values(user_id=user_id, secret=secret)
        try:
            await session.execute(statement)
            await session.commit()
        except SQLAlchemyError as err:
            await log_exception(err)

#Retrieve 2FA
async def get_2fa(user_id) -> TwoFA | None:
    async with async_session() as session:
        statement = sa.select(TwoFA).where(TwoFA.user_id == user_id)
        result = await session.execute(statement)
        twoFA = result.scalars().first()
        if twoFA:
            return twoFA
        else:
            return None

#Check if 2FA exists
async def check_2fa_exists(user_id) -> bool:
    async with async_session() as session:
        statement = sa.select(TwoFA).where(TwoFA.user_id == user_id)
        result = await session.execute(statement)
        twoFA = result.scalars().first()
        if twoFA:
            return True
        else:
            return False

#Delete 2FA
async def delete_2fa(user_id):
    async with async_session() as session:
        statement = sa.delete(TwoFA).where(TwoFA.user_id == user_id)
        try:
            await session.execute(statement)
            await session.commit()
        except SQLAlchemyError as err:
            await session.rollback()
            await log_exception(err)