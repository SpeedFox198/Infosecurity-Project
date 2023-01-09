import os

import socketio
import sqlalchemy as sa
from db_access.globals import async_session
from models import AuthedUser, Group, Media, Membership, Message, Room, User
from socketio.exceptions import ConnectionRefusedError
from sqlalchemy.orm.exc import NoResultFound
from utils import secure_save_file, to_unix

from .disappearing import DisappearingQueue
from .sio_auth_manager import SioAuthManager
from .functions import get_display_dimensions

ASYNC_MODE = "asgi"
CORS_ALLOWED_ORIGINS = "https://localhost"
SIO_SESSION_USER_KEY = "user"
MESSAGE_LOAD_NUMBER = 20  # Number of messages to load at once


sio = socketio.AsyncServer(async_mode=ASYNC_MODE, cors_allowed_origins=CORS_ALLOWED_ORIGINS)

# Create and get a queue disappearing messages
messages_queue = DisappearingQueue()

sio_auth_manager = SioAuthManager()  # Authentication Manager

# TODO(medium)(SpeedFox198): logging
@sio.event
async def connect(sid, environ, auth):
    """ Event when client connects to server """
    current_user = sio_auth_manager.get_user(environ["HTTP_COOKIE"])

    if not await current_user.is_authenticated:
        raise ConnectionRefusedError("authentication failed")

    # Save user session
    await save_user(sid, current_user)

    # Add client to their respective rooms
    rooms = await get_room(await current_user.user_id)

    for room in rooms:
        sio.enter_room(sid, room["room_id"])
    # print(f"{sid} joined: {sio.rooms(sid)}")

    # Send room_ids that client belongs to
    await sio.emit("rooms_joined", rooms, to=sid)


@sio.event
async def disconnect(sid):
    """ Event when client disconnects from server """
    # TODO(medium)(SpeedFox198): change to log later
    # print("disconnected:", sid)


# TODO(medium)(SpeedFox198): authenticate and verify msg (and format)
@sio.event
async def send_message(sid, data: dict):
    # print(f"Received {data}")  # TODO(medium)(SpeedFox198): change to log later
    print("here"*12)

    message_data = data["message"]
    file = data.get("file", None)
    filename = data.get("filename", None)

    # Get user from session
    user = await get_user(sid)
    user_id = await user.user_id

    # Insert object into database
    async with async_session() as session:
        # Get room
        statement = sa.select(Room).where(Room.room_id == message_data["room_id"])

        try:
            async with session.begin():
                result = (await session.execute(statement)).one()
        except NoResultFound:
            return  # If room not found, abort adding of message
        else:
            room = result[0]

        # Create message object
        message = Message(
            user_id,
            room.room_id,
            message_data["content"],
            message_data["reply_to"],  # TODO(low)(SpeedFox198): remove if unused
            message_data["type"]
        )

        # Add message to database
        async with session.begin():
            session.add(message)

        # Save file if message type is not text, and file exists
        # TODO(high)(SpeedFox198): test what happens when upload file of size 0 bytes lmao
        if message.type != "text" and file:
            destination_directory = os.path.join(
                sio_auth_manager.app.config["ATTACHMENTS_PATH"],
                message.room_id,
                message.message_id
            )
            os.makedirs(destination_directory)
            filename = await secure_save_file(destination_directory, filename, file)

            media = Media(message.message_id, path=filename)
            async with session.begin():
                session.add(media)

    # If room has disappearing messages enabled
    if room.disappearing:
        await messages_queue.add_disappearing_messages(message.message_id, seconds=15)

    # Forward messages to other clients in same room
    await sio.emit("receive_message", {
        "message_id": message.message_id,
        "room_id": message.room_id,
        "user_id": message.user_id,
        "time": to_unix(message.time),
        "content": message.content,
    }, room=message_data["room_id"], skip_sid=sid)

    # Return timestamp and message_id to client
    await sio.emit("sent_success", {
        "message_id": message.message_id,
        "room_id": message.room_id,
        "temp_id": message_data["message_id"],
        "time": to_unix(message.time),
        "filename": filename
    }, to=sid)
    print("here", filename)


# TODO(medium)(SpeedFox198): authenticate and verify msg (and format)
@sio.event
async def get_room_messages(sid, data):
    print(f"Received {data}")  # TODO(medium)(SpeedFox198): change to log later
    room_id = data["room_id"]
    n = data["n"]
    extra = data["extra"]
    limit = MESSAGE_LOAD_NUMBER
    offset = MESSAGE_LOAD_NUMBER * n + extra

    # Get room messages from database
    async with async_session() as session:
        statement = sa.select(
            Message.message_id,
            Message.user_id,
            Message.time,
            Message.content,
            Message.type
        ).where(
            Message.room_id == room_id
        ).order_by(Message.time.desc()).limit(limit).offset(offset)

        result = (await session.execute(statement)).all()
        room_messages = [{
            "message_id": result[i].message_id,
            "user_id": result[i].user_id,
            "time": to_unix(result[i].time),
            "content": result[i].content,
            "type": result[i].type
        } for i in range(len(result) - 1, -1, -1)]

    await sio.emit("receive_room_messages", {
        "room_id": room_id,
        "room_messages": room_messages
    }, to=sid)


# TODO(medium)(SpeedFox198): delete media if exists
# TODO(medium)(SpeedFox198): authenticate and verify msg (and format)
# ensure user is part of room and is admin
# ensure data in correct format, (length of data also?)
@sio.event
async def delete_messages(sid, data):
    print(f"Received {data}")  # TODO(medium)(SpeedFox198): change to log later

    messages = data["messages"]
    room_id = data["room_id"]

    # Get user from session
    user = await get_user(sid)
    user_id = await user.user_id

    # Delete messages from database (ensures that room_id is correct)
    async with async_session() as session:

        # Get room type details
        statement = sa.select(Room.type).where(Room.room_id == room_id)
        room_type = (await session.execute(statement)).one()[0]

        if room_type == "direct":  # User's can't delete other's messages in direct chats
            is_admin = False
        else:
            # Check if user is group admin
            statement = sa.select(Membership.is_admin).where(
                (Membership.user_id == user_id)
                & (Membership.room_id == room_id)
            )
            is_admin = (await session.execute(statement)).one()[0]

        condition = (Message.message_id.in_(messages)) & (Message.room_id == room_id)

        # If user is not admin of group chat, only allow deletion of own messages
        if not is_admin:
            condition &= (Message.user_id == user_id)

        # Get messages to delete
        statement = sa.select(Message.message_id).where(condition)

        result = (await session.execute(statement)).all()
        messages = [row[0] for row in result]

        # Delete messages from database
        statement = sa.delete(Message).where(Message.message_id.in_(messages))
        await session.execute(statement)

        await session.commit()

    # Tell other clients in same room to delete the same messages
    await delete_client_messages(messages, room_id)
    # TODO(UI)(SpeedFox198): skip_sid=sid (client side must del 1st)
    # ^ maybe not? (im lazy)


async def save_user(sid: str, user: AuthedUser) -> None:
    """ Save user object to sio session """
    await sio.save_session(sid, {SIO_SESSION_USER_KEY: user})


async def get_user(sid: str) -> AuthedUser | None:
    """ Returns user object from sio session """
    return (await sio.get_session(sid)).get(SIO_SESSION_USER_KEY, None)


async def get_room(user_id: str):
    async with async_session() as session:

        # Retrieve room and membership info of user
        statement = sa.select(
            Room.room_id, Room.disappearing, Room.type, Membership.is_admin
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
            "is_admin": row[3],
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

    for room_id, messages in deleted.items():
        await delete_client_messages(messages, room_id)


async def delete_client_messages(messages, room_id, skip_sid=None):
    """ Inform other clients in room to delete messages """
    await sio.emit("message_deleted", {
        "messages": messages,
        "room_id": room_id
    }, room=room_id, skip_sid=skip_sid)


async def job_disappear_messages():
    # print("Job ran")  # TODO(medium)(SpeedFox198): Change to log
    await messages_queue.check_disappearing_messages(delete_expired_messages)


async def task_disappear_messages(scheduler):
    """ Task to run scheduled checking for disappearing of messages """
    scheduler.add_job(job_disappear_messages, "interval", seconds=5)
    scheduler.start()
