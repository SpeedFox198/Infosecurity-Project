from ua_parser import user_agent_parser
import aiohttp


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

            return f"{data['regionName']}, {data['country']}"


