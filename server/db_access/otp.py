import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError

import models
from db_access.globals import async_session
from utils.logging import log_exception


# Create OTP
async def create_otp(email, otp, password) -> None:
    async with async_session() as session:
        statement = sa.insert(models.OTP).values(email=email, otp=otp, password=password)
        try:
            await session.execute(statement)
            await session.commit()
        except SQLAlchemyError as err:
            await log_exception(err)


# Retrieve OTP
async def get_otp(email) -> models.OTP | None:
    async with async_session() as session:
        statement = sa.select(models.OTP).where(models.OTP.email == email)
        result = await session.execute(statement)
        otp = result.scalars().first()
        if otp:
            return otp


# Delete OTP
async def delete_otp(email):
    async with async_session() as session:
        statement = sa.delete(models.OTP).where(models.OTP.email == email)
        try:
            await session.execute(statement)
            await session.commit()
        except SQLAlchemyError:
            return False
