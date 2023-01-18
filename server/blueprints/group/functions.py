import os
from uuid import uuid4

from quart.datastructures import FileStorage
from PIL import Image

from models import Room


async def resize_image(path: str | os.PathLike) -> None:
    output_size = (128, 128)
    icon_resizer = Image.open(path)
    icon_resizer.thumbnail(output_size)
    icon_resizer.save(path)


async def save_group_icon(room: Room, group_icon: FileStorage) -> os.PathLike | str:
    """ Returns the group icon path for future reference"""
    icon_base_path = os.path.join("media/icon", room.room_id)
    extension: str = group_icon.filename.split(".")[1]
    icon_path: os.PathLike | str = os.path.join(icon_base_path, f"{str(uuid4())}.{extension}")
    await group_icon.save(icon_path)
    return icon_path
