from sqlalchemy.ext.asyncio import AsyncSession
from ua_parser import user_agent_parser
import aiohttp

# TODO(br1ght) do functions for manage devices


async def add_logged_in_device(sql_session: AsyncSession, user_agent: str) -> None:
    parsed: dict[str, str] = user_agent_parser.Parse(user_agent)


async def get_location_from_ip(ip_address: str) -> str:
    unknown_country = "Unknown, Unknown"
    api_link = f"http://ip-api.com/json/{ip_address}?fields=49183"

    async with aiohttp.ClientSession() as session:
        async with session.get(api_link) as response:

            if not response.ok:
                return unknown_country

            data = await response.json()

            if data["status"] == "fail":
                return unknown_country

            return f"{data['country']}, {data['regionName']}"
