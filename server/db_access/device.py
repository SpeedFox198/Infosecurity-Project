from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from db_access.globals import async_session
import sqlalchemy as sa

from models import Device
from utils.logging import log_exception


async def add_logged_in_device(sql_session, device_id: str, user_id: str, browser: str, os: str, location: str) -> None:
    statement = sa.insert(Device).values(device_id=device_id,
                                         user_id=user_id,
                                         time=datetime.now(),
                                         location=location,
                                         os=os,
                                         browser=browser)
    try:
        await sql_session.execute(statement)
        await sql_session.commit()
    except SQLAlchemyError:
        await sql_session.rollback()
        await log_exception()


async def remove_logged_in_device(device_id: str, user_id: str) -> str:
    async with async_session() as session:
        statement = sa.delete(Device).where((Device.device_id == device_id) & (Device.user_id == user_id))
        try:
            await session.execute(statement)
            await session.commit()
            return "success"
        except SQLAlchemyError:
            await session.rollback()
            await log_exception()
            return "fail"


async def get_device(user_id: str, device_id: str):
    async with async_session() as session:
        statement = sa.select(Device).where(
            (Device.user_id == user_id)
            &
            (Device.device_id == device_id)
        )

        try:
            result = await session.execute(statement)
            return result.scalars().first()
        except SQLAlchemyError:
            await session.rollback()
            await log_exception()
