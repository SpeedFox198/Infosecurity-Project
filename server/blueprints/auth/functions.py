from ua_parser import user_agent_parser
import aiohttp
import secrets
import string

from google_authenticator.google_email_send import gmail_send


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

def generate_otp() -> str:
    # Generate a 6 digit OTP
    return "".join(secrets.choice(string.digits) for i in range(6))

def send_otp_email(email: str, otp: str):
    subject = "OTP for registration"
    message = f"Do not reply to this email.\nPlease enter {otp} as your OTP to complete your registration."
    gmail_send(email, subject, message)

#Account lockout alert
def send_alert_email(email: str):
    subject = "Account lockout alert"
    message = f"Do not reply to this email.\nYour account has been locked out due to too many failed login attempts. If it was not you, please change your password."
    gmail_send(email, subject, message)