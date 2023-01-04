import os
import time
from datetime import datetime
from uuid import uuid4

from aiofiles import open as async_open
from werkzeug.utils import secure_filename


def to_unix(timestamp:datetime) -> int:
    """
    Convert datetime object to unix time format

    Args:
        timestamp(datetime): timestamp to be converted

    Returns:
        int: Unix time format of timestamp
    """
    return int(time.mktime(timestamp.timetuple()))



async def secure_save_file(directory: str, filename: str, data: bytes) -> str:
    """
    Santises and returns secure filename before saving data in specified directory

    Assumes directory is secure
    """

    # Ensure filename is secure
    name, extension = os.path.splitext(filename)
    name = secure_filename(name)
    if name == "":  # Assign random name if name is empty
        name = str(uuid4())
    if extension != "":
        extension = "." + secure_filename(extension)

    filename = name + extension

    # Save file in directory
    await save_file_directory(directory, filename, data)

    # Return sanitised filename
    return filename


async def save_file_directory(directory: str, filename: str, data: bytes):
    destination = os.path.join(directory, filename)
    await save_file(destination, data)


async def save_file(destination: str, data: bytes):
    async with async_open(destination, "wb") as file:
        await file.write(data)
