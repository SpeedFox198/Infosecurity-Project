import os
from io import BytesIO

import sqlalchemy as sa
from db_access.globals import async_session
from models import Group, Media, Membership, Message, Room, User
from PIL import Image
from utils import secure_save_file

from .disappearing import DisappearingQueue

# Create and get a queue disappearing messages
messages_queue = DisappearingQueue()


def get_display_dimensions(picture: bytes):
    """ Generates the height and width to display picture """

    image = Image.open(BytesIO(picture))
    width = image.width
    height = image.height
    print(f"\n\nwidth: {width}, height: {height}\n\n")

    ratio = height / width
    if ratio > 1:
        width = 300
    else:
        width = 400

    height = round(width*ratio, 3)

    if height > 440:
        height = 440
    elif height < 100:
        height = 100

    return height, width


async def save_file(attachments_path: str, file: bytes, filename: str, room_id: str, message_id: str, session):
    """ Save file securely I guess (returns image filename, height, and width) """

    destination_directory = os.path.join(attachments_path, room_id, message_id)
    os.makedirs(destination_directory)
    filename = await secure_save_file(destination_directory, filename, file)

    # TODO(high)(SpeedFox198): Check if file is image (check what kind of file)
    height, width = get_display_dimensions(file)

    media = Media(message_id, path=filename, height=height, width=width)
    async with session.begin():
        session.add(media)

    return filename, height, width


async def get_room(user_id: str):
    async with async_session() as session:

        # Retrieve room and membership info of user
        statement = sa.select(
            Room.room_id, Room.disappearing, Room.type, Room.encrypted, Membership.is_admin
        ).join_from(
            Room, Membership
        ).where(
            Membership.user_id == user_id
        )
        result = (await session.execute(statement)).all()

        # Unpack retrieved values
        rooms = [{
            "room_id": row[0],
            "disappearing": row[1],
            "type": row[2],
            "encrypted": row[3],
            "is_admin": row[4]
        } for row in result]

        # Retrieve additional room details for UI
        for room in rooms:
            if room["type"] == "direct":
                statement = sa.select(User.username, User.avatar).where(
                    User.user_id == sa.select(Membership.user_id).where(
                        (Membership.room_id == room["room_id"]) &
                        (Membership.user_id != user_id)
                    ).scalar_subquery()
                )
                result = (await session.execute(statement)).one()
            elif room["type"] == "group":
                statement = sa.select(Group.name, Group.icon).where(Group.room_id == room["room_id"])
                result = (await session.execute(statement)).one()
            else:
                continue  # Just in case hahaha
            room["name"] = result[0]
            room["icon"] = result[1]

    return rooms


async def delete_expired_messages(messages):
    async with async_session() as session:
        statement = sa.select(Message.message_id, Message.room_id).where(Message.message_id.in_(messages))
        result = (await session.execute(statement)).fetchall()
        filter_ids = [row[0] for row in result]

        statement = sa.delete(Media).where(Media.message_id.in_(filter_ids))
        await session.execute(statement)
        statement = sa.delete(Message).where(Message.message_id.in_(filter_ids))
        await session.execute(statement)

        await session.commit()

    # Format a dictionary of deleted messages
    deleted = {}
    for row in result:
        messages = deleted.get(row[1], [])
        if not messages:
            deleted[row[1]] = messages
        messages.append(row[0])

    return deleted


async def save_group_icon(room_id: str, group_icon_name: str, group_icon: bytes) -> os.PathLike | str:
    """ Returns the group icon path for future reference"""
    icon_base_path = os.path.join("media/icon", room_id)
    os.makedirs(icon_base_path)
    saved_group_icon_name = await secure_save_file(icon_base_path, group_icon_name, group_icon)
    return os.path.join(icon_base_path, saved_group_icon_name)