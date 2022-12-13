from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from db_access.globals import async_session
import sqlalchemy as sa

from models import Device
from utils.logging import log_exception


async def add_logged_in_device(sql_session,
                               device_id: str,
                               user_id: str,
                               browser: str,
                               os: str,
                               location: str) -> None:
    statement = sa.insert(Device).values(device_id=device_id,
                                         user_id=user_id,
                                         time=datetime.now(),
                                         location=location,
                                         os=os,
                                         browser=browser)
    try:
        await sql_session.execute(statement)
        await sql_session.commit()
    except SQLAlchemyError as err:
        await sql_session.rollback()
        await log_exception(err)


async def remove_logged_in_device(device_id: str, user_id: str) -> bool:
    async with async_session() as session:
        delete_device_statement = sa.delete(Device).where((Device.device_id == device_id) & (Device.user_id == user_id))

        # Try to delete the selected device
        try:
            await session.execute(delete_device_statement)
            await session.commit()
        except SQLAlchemyError as err:
            await session.rollback()
            await log_exception(err)
            return False

        check_deleted_device_statement = sa.exists(
            sa.select(Device)
            .where((Device.device_id == device_id) & (Device.user_id == user_id))
        )

        try:
            device_exists = (await session.execute(
                sa.select(Device)
                .where(check_deleted_device_statement)
            )).scalar()

            if device_exists is not None:
                return False

            return True
        except SQLAlchemyError as err:
            await session.rollback()
            await log_exception(err)
            return False


async def get_device(user_id: str, device_id: str) -> Device | None:
    async with async_session() as session:
        statement = sa.select(Device).where(
            (Device.user_id == user_id)
            &
            (Device.device_id == device_id)
        )

        try:
            result = await session.execute(statement)
            return result.scalars().first()
        except SQLAlchemyError as err:
            await session.rollback()
            await log_exception(err)
