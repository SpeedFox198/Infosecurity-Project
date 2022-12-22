from datetime import datetime

from quart import render_template
from ua_parser import user_agent_parser
import aiohttp
import secrets
import string

from google_authenticator.google_email_send import gmail_send
from models import User


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
    return "".join(secrets.choice(string.digits) for _ in range(6))


def send_otp_email(email: str, otp: str):
    subject = "OTP for registration"
    message = f"Do not reply to this email.\nPlease enter {otp} as your OTP to complete your registration."
    gmail_send(email, subject, message)


def send_password_recovery_email(email: str, token: str):
    subject = "OTP for password recovery"
    message = f"Do not reply to this email.\nPlease click on this link to reset your password." + token
    gmail_send(email, subject, message)


# Account lockout alert
def send_lockout_alert_email(email: str):
    subject = "Account lockout alert"
    message = f"Do not reply to this email.\nYour account has been locked out due to too many failed login attempts. If it was not you, please change your password."
    gmail_send(email, subject, message)


async def send_login_alert_email(user: User,
                                 browser: str,
                                 os: str,
                                 location: str,
                                 ip_addr: str) -> None:
    current_date = datetime.utcnow().strftime("%d %B %Y, %H:%M:%S UTC")
    subject = "Your Bubbles Account - Successful Log-in"
    message = await render_template("login_alert.html",
                                    user=user,
                                    browser=browser,
                                    os=os,
                                    location=location,
                                    date=current_date,
                                    ip_addr=ip_addr
                                    )
    gmail_send(user.email, subject, message)
