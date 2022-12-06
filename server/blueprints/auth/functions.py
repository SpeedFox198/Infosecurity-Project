from datetime import datetime

import quart
from sqlalchemy.exc import SQLAlchemyError
import sqlalchemy as sa
from ua_parser import user_agent_parser
import aiohttp

from db_access.globals import async_session
from models import Device


async def get_user_agent_data(user_agent: str) -> tuple[str, str]:
    parsed = user_agent_parser.Parse(user_agent)
    browser_data = parsed["user_agent"]
    os_data = parsed["os"]
    return browser_data["family"], os_data["family"]


async def get_location_from_ip(ip_address: str) -> str:
    unknown_country = "Unknown, Unknown"
    api = f"http://ip-api.com/json/{ip_address}?fields=49183"

    async with aiohttp.ClientSession() as http_session:
        async with http_session.get(api) as response:

            if not response.ok:
                return unknown_country

            data = await response.json()

            if data["status"] == "fail":
                return unknown_country

            return f"{data['country']}, {data['regionName']}"


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
        raise err


async def remove_logged_in_device(device_id: str, user_id: str) -> None:
    with async_session() as session:
        statement = sa.delete(Device).where((Device.device_id == device_id) & (Device.user_id == user_id))
        try:
            await session.execute(statement)
            await session.commit()
        except SQLAlchemyError as err:
            await session.rollback()
            raise err
