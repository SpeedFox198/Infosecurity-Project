import logging
from logging.handlers import TimedRotatingFileHandler, SysLogHandler
from datetime import datetime

from quart import request

PAPERTRAIL_HOST = "logs4.papertrailapp.com"
PAPERTRAIL_PORT = 22206

logger = logging.getLogger("bubbles_log")
logger.setLevel(logging.INFO)

# Log setup to rotate to new files every midnight
log_name = f"logs/{datetime.now().strftime('%d-%m-%Y')}-app.log"
log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s",
                               datefmt="%d-%m-%Y %H:%M:%S")

file_handler = TimedRotatingFileHandler(log_name, when="midnight", interval=1)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(log_format)

syslog_handler = SysLogHandler(address=(PAPERTRAIL_HOST, PAPERTRAIL_PORT))
syslog_handler.setLevel(logging.INFO)
syslog_handler.setFormatter(log_format)

logger.addHandler(file_handler)
logger.addHandler(syslog_handler)

# For debugging on screen
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_format)
logger.addHandler(stream_handler)


async def log_warning(message: str) -> None:
    logger.warning(message)


async def log_error(message: str) -> None:
    logger.error(message)


async def log_info(message: str) -> None:
    logger.info(message)


async def log_critical(message: str) -> None:
    logger.critical(message)


async def log_exception(error: Exception) -> None:
    await log_error(f"Exception {type(error).__name__} happened at {request.path}, Description: {error}")
