import os
from uuid import uuid4

from quart.datastructures import FileStorage

from models import Room


async def save_group_icon(room: Room, group_icon: FileStorage) -> os.PathLike | str:
    """ Returns the group icon path for future reference"""
    icon_base_path = os.path.join("media/icon", room.room_id)
    extension: str = group_icon.filename.split(".")[1]
    icon_path: os.PathLike | str = os.path.join(icon_base_path, f"{uuid4()}.{extension}")
    os.makedirs(icon_base_path)
    await group_icon.save(icon_path)
    return icon_path
