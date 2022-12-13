import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

logger = logging.getLogger("bubbles_log")
logger.setLevel(logging.INFO)

# Log setup to rotate to new files every midnight
log_name = f"logs/{datetime.now().strftime('%d-%m-%Y')}-app.log"
log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

file_handler = TimedRotatingFileHandler(log_name, when="midnight", interval=1)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(log_format)

logger.addHandler(file_handler)

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
