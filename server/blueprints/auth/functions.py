from datetime import datetime

from quart import render_template
from ua_parser import user_agent_parser
import aiohttp
import secrets
import string

from db_access.account_lockout import create_lockout, get_email
from db_access.failed_attempt import create_failed_attempt, update_failed_attempt, get_failed_attempt, \
    delete_failed_attempt
from google_authenticator.google_email_send import gmail_send
from models import User
from models.general.BrowsingData import BrowsingData
from utils.logging import log_info, log_warning


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


async def evaluate_failed_attempts(existing_user: User,
                                   invalid_cred_response: tuple[dict[str, str], int],
                                   browsing_data: BrowsingData) -> tuple[dict[str, str], int]:

    failed_attempt = (await get_failed_attempt(existing_user.user_id))

    # Check if a failed attempt exists
    if failed_attempt is None:
        await create_failed_attempt(existing_user.user_id)
        await log_info(f"User {existing_user.username} has failed to log in using {browsing_data.browser}, {browsing_data.os} from {browsing_data.location}")
        return invalid_cred_response

    if 5 > failed_attempt.attempts > 0:
        await update_failed_attempt(failed_attempt.user_id, (failed_attempt.attempts + 1))
        await log_info(f"User {existing_user.username} has failed to log in using {browsing_data.browser}, {browsing_data.os} from {browsing_data.location}")
        return invalid_cred_response

    if failed_attempt.attempts == 5:
        await create_lockout(failed_attempt.user_id)
        await delete_failed_attempt(failed_attempt.user_id)

        lockout_user_email = await get_email(failed_attempt.user_id)
        send_lockout_alert_email(lockout_user_email)

        await log_warning(f"User {existing_user.username} has been locked out for 30 minutes.")
        return invalid_cred_response


async def generate_otp() -> str:
    # Generate a 6 digit OTP
    return "".join(secrets.choice(string.digits) for _ in range(6))


def send_otp_email(email: str, otp: str):
    subject = "OTP for registration"
    message = f"Do not reply to this email.\nPlease enter {otp} as your OTP to complete your registration."
    gmail_send(email, subject, message)


def send_password_recovery_email(email: str, token: str):
    link = f"https://localhost/reset-password?token={token}"
    subject = "Link for password recovery"
    message = f"Do not reply to this email.\nPlease click on this link to reset your password." + link
    gmail_send(email, subject, message)


# Account lockout alert
def send_lockout_alert_email(email: str):
    subject = "Account lockout alert"
    message = f"Do not reply to this email.\nYour account has been locked out due to too many failed login attempts. If it was not you, please change your password."
    gmail_send(email, subject, message)


async def send_login_alert_email(user: User,
                                 browsing_data: BrowsingData,
                                 ip_addr: str) -> None:
    current_date = datetime.utcnow().strftime("%d %B %Y, %H:%M:%S UTC")
    subject = "Your Bubbles Account - Successful Log-in"
    message = await render_template("login_alert.html",
                                    user=user,
                                    browser=browsing_data.browser,
                                    os=browsing_data.os,
                                    location=browsing_data.location,
                                    date=current_date,
                                    ip_addr=ip_addr
                                    )
    gmail_send(user.email, subject, message)
