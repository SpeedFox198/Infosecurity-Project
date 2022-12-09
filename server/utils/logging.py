from app import app

logger = app.logger


async def log_warning(message: str) -> None:
    logger.warning(message)


async def log_error(message: str) -> None:
    logger.error(message)


async def log_info(message: str) -> None:
    logger.info(message)


async def log_exception() -> None:
    logger.exception()
