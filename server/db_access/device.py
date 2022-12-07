from datetime import datetime

import quart
from sqlalchemy.exc import SQLAlchemyError

from blueprints.auth.functions import get_user_agent_data, get_location_from_ip
from db_access.globals import async_session
import sqlalchemy as sa

from models import Device


async def add_logged_in_device(sql_session, device_id: str, user_id: str, request: quart.Request) -> None:
    browser, os = await get_user_agent_data(request.user_agent.string)
    location = await get_location_from_ip(request.remote_addr)
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
        print(err)


async def remove_logged_in_device(device_id: str, user_id: str) -> str:
    async with async_session() as session:
        statement = sa.delete(Device).where((Device.device_id == device_id) & (Device.user_id == user_id))
        try:
            await session.execute(statement)
            await session.commit()
            return "success"
        except SQLAlchemyError as err:
            await session.rollback()
            print(err)
            return "fail"
