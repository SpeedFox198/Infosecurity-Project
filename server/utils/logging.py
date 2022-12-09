import logging


async def log_warning(message: str) -> None:
    logging.warning(message)


async def log_error(message: str) -> None:
    logging.error(message)


async def log_info(message: str) -> None:
    logging.info(message)


async def log_exception() -> None:
    logging.exception("Exception happened")
