import socketio
import sqlalchemy as sa
from pydantic import ValidationError

from db_access.globals import async_session
from db_access.sio import (
    set_online_status,
    add_sio_connection,
    remove_sio_connection,
    get_sid_from_sio_connection,
    remove_friend_request
)
from db_access.user import get_user_details
from models import AuthedUser, Disappearing, Media, Membership, Message, Room, Group, FriendRequest, Friend
from socketio.exceptions import ConnectionRefusedError
from sqlalchemy.orm.exc import NoResultFound

from models.request_data import GroupMetadataBody
from utils import to_unix

from .functions import delete_expired_messages, get_room, messages_queue, save_file, save_group_icon
from .sio_auth_manager import SioAuthManager

ASYNC_MODE = "asgi"
CORS_ALLOWED_ORIGINS = "https://localhost"
MAX_HTTP_BUFFER_SIZE = 5000000  # 5 megabyte payload limit
SIO_SESSION_USER_KEY = "user"
MESSAGE_LOAD_NUMBER = 20  # Number of messages to load at once

sio = socketio.AsyncServer(
    async_mode=ASYNC_MODE,
    cors_allowed_origins=CORS_ALLOWED_ORIGINS,
    max_http_buffer_size=MAX_HTTP_BUFFER_SIZE
)

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

    await set_online_status(await current_user.user_id, True)
    await add_sio_connection(sid, await current_user.user_id)

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
    current_user = await get_user(sid)
    await set_online_status(await current_user.user_id, False)
    await remove_sio_connection(sid, await current_user.user_id)


# TODO(medium)(SpeedFox198): authenticate and verify msg (and format)
@sio.event
async def send_message(sid, data: dict):
    # print(f"Received {data}")  # TODO(medium)(SpeedFox198): change to log later

    message_data = data["message"]
    file = data.get("file", None)
    filename = data.get("filename", None)
    height = width = None  # Initialise height and width values

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
            room: Room = result[0]

        # Create message object
        message = Message(
            user_id,
            room.room_id,
            message_data["content"],
            reply_to=message_data["reply_to"],  # TODO(low)(SpeedFox198): remove if unused
            type_=message_data["type"],
            encrypted=room.encrypted
        )

        # Add message to database
        async with session.begin():
            session.add(message)

        # Save file if message type is not text, and file exists
        # TODO(high)(SpeedFox198): test what happens when upload file of size 0 bytes lmao
        if message.type != "text" and file:
            await save_file(
                sio_auth_manager.app.config["ATTACHMENTS_PATH"],
                file, filename, message.room_id, message.message_id, session)

    # If room has disappearing messages enabled
    if room.disappearing != "off":
        days = {"24h": 1, "7d": 7, "30d": 30}[room.disappearing]
        await messages_queue.add_disappearing_messages(message.message_id, days=days)

    # Forward messages to other clients in same room
    await sio.emit("receive_message", {
        "message_id": message.message_id,
        "room_id": message.room_id,
        "user_id": message.user_id,
        "time": to_unix(message.time),
        "content": message.content,
    }, room=message_data["room_id"], skip_sid=sid)

    # Return timestamp and message_id to client
    data = {
        "message_id": message.message_id,
        "room_id": message.room_id,
        "temp_id": message_data["message_id"],
        "time": to_unix(message.time),
        "filename": filename
    }
    if filename:
        data["filename"] = filename
    if height and width:
        data["height"] = height
        data["width"] = width
    await sio.emit("sent_success", data, to=sid)


# TODO(medium)(SpeedFox198): authenticate and verify msg (and format)
@sio.event
async def get_room_messages(sid, data):
    # print(f"Received {data}")  # TODO(medium)(SpeedFox198): change to log later
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
            Message.type,
            Message.encrypted
        ).where(
            Message.room_id == room_id
        ).order_by(Message.time.desc()).limit(limit).offset(offset)

        result: list[Message] = (await session.execute(statement)).all()
        room_messages = [{
            "message_id": result[i].message_id,
            "user_id": result[i].user_id,
            "time": to_unix(result[i].time),
            "content": result[i].content,
            "type": result[i].type,
            "encrypted": result[i].encrypted
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
        statement = sa.delete(Media).where(Media.message_id.in_(messages))
        await session.execute(statement)

        statement = sa.delete(Disappearing).where(Disappearing.message_id.in_(messages))
        await session.execute(statement)

        statement = sa.delete(Message).where(Message.message_id.in_(messages))
        await session.execute(statement)

        await session.commit()

    # Tell other clients in same room to delete the same messages
    await delete_client_messages(messages, room_id)
    # TODO(UI)(SpeedFox198): skip_sid=sid (client side must del 1st)
    # ^ maybe not? (im lazy)


@sio.event
async def create_group(sid, data):
    # print(f"Received {data}")
    current_user = await get_user(sid)

    try:
        group_metadata = GroupMetadataBody(**data)
    except ValidationError as err:
        error_list = [error["msg"] for error in err.errors()]
        error_message = error_list[0]
        await sio.emit("create_group_error", {
            "message": error_message
        }, to=sid)
        return

    async with async_session() as session:
        # Create new room
        new_room = Room(group_metadata.disappearing, "group")
        session.add(new_room)
        await session.flush()

        if group_metadata.icon and group_metadata.icon_name:
            # Add Group icon if any and the group details
            icon_path = await save_group_icon(new_room, group_metadata.icon_name, group_metadata.icon)

            session.add(
                Group(new_room.room_id, group_metadata.name, icon_path)
            )
            await session.flush()
        else:
            session.add(
                Group(new_room.room_id, group_metadata.name)
            )
            await session.flush()

        # Add the current user as admin of the group
        session.add(
            Membership(new_room.room_id, await current_user.user_id, is_admin=True)
        )
        await session.flush()

        # Add the included users to the group
        for user_id in group_metadata.users:
            session.add(
                Membership(new_room.room_id, user_id)
            )
            await session.flush()

        await session.commit()

    await sio.emit("group_created", to=sid)

    # Emit event to update users they have been added to group
    for user_id in (group_metadata.users + [await current_user.user_id]):
        user_sid = await get_sid_from_sio_connection(user_id)
        if user_sid is None:
            continue

        rooms = await get_room(user_id)
        for room in rooms:
            sio.enter_room(user_sid, room["room_id"])

        # Send room_ids that client belongs to
        await sio.emit("group_invite", rooms, to=user_sid)


@sio.event
async def send_friend_request(sid: str, data: dict):
    current_user = await get_user(sid)
    recipient_id = data.get("user")
    if recipient_id is None:
        await sio.emit("friend_request_failed", {
            "message": "Invalid user"
        }, to=sid)
        return

    valid_user = await get_user_details(recipient_id)
    if valid_user is None:
        await sio.emit("friend_request_failed", {
            "message": "Invalid user"
        }, to=sid)
        return

    async with async_session() as session:
        fr_made_before_statement = sa.select(FriendRequest).where(
            (FriendRequest.sender == await current_user.user_id) &
            (FriendRequest.recipient == recipient_id)
        )
        friend_request_made_before: FriendRequest | None = (await session.execute(fr_made_before_statement)).first()
        if friend_request_made_before:
            await sio.emit("friend_request_failed", {
                "message": "Request was sent previously"
            }, to=sid)
            return

        session.add(
            FriendRequest(sender=await current_user.user_id,
                          recipient=recipient_id)
        )
        await session.commit()

    await sio.emit("friend_request_sent", data=recipient_id, to=sid)


@sio.event
async def cancel_sent_friend_request(sid: str, data: dict):
    print(f"Received {data}")
    current_user = await get_user(sid)

    recipient_id = data.get("user")
    if recipient_id is None:
        await sio.emit("failed_cancel_friend_request", {
            "message": "Invalid user"
        }, to=sid)
        return

    valid_recipient = await get_user_details(recipient_id)
    if valid_recipient is None:
        await sio.emit("failed_cancel_friend_request", {
            "message": "Invalid user"
        }, to=sid)
        return

    await remove_friend_request(await current_user.user_id, recipient_id)
    await sio.emit("friend_requests_update", to=sid)

    recipient_sid = await get_sid_from_sio_connection(recipient_id)
    if recipient_sid:
        await sio.emit("friend_requests_update", to=recipient_sid)


@sio.event
async def accept_friend_request(sid: str, data: dict):
    print(f"Received {data}")
    current_user = await get_user(sid)

    sender_id = data.get("user")
    if sender_id is None:
        await sio.emit("failed_accept_friend_request", {
            "message": "Invalid user"
        }, to=sid)
        return

    valid_sender = await get_user_details(sender_id)
    if valid_sender is None:
        await sio.emit("failed_accept_friend_request", {
            "message": "Invalid user"
        }, to=sid)
        return

    await remove_friend_request(sender_id, await current_user.user_id)
    async with async_session() as session:
        session.add(Friend(sender_id, await current_user.user_id))
        await session.commit()

    await sio.emit("friend_requests_update", to=sid)

    sender_sid = await get_sid_from_sio_connection(sender_id)
    if sender_sid:
        await sio.emit("friend_requests_update", to=sender_sid)


@sio.event
async def cancel_received_friend_request(sid: str, data):
    print(f"Received {data}")
    current_user = await get_user(sid)

    sender_id = data.get("user")
    if sender_id is None:
        await sio.emit("failed_accept_friend_request", {
            "message": "Invalid user"
        }, to=sid)
        return

    valid_sender = await get_user_details(sender_id)
    if valid_sender is None:
        await sio.emit("failed_accept_friend_request", {
            "message": "Invalid user"
        }, to=sid)
        return

    await remove_friend_request(sender_id, await current_user.user_id)
    await sio.emit("friend_requests_update", to=sid)

    sender_sid = await get_sid_from_sio_connection(sender_id)
    if sender_sid:
        await sio.emit("friend_requests_update", to=sender_sid)


async def save_user(sid: str, user: AuthedUser) -> None:
    """ Save user object to sio session """
    await sio.save_session(sid, {SIO_SESSION_USER_KEY: user})


async def get_user(sid: str) -> AuthedUser | None:
    """ Returns user object from sio session """
    return (await sio.get_session(sid)).get(SIO_SESSION_USER_KEY, None)


async def delete_client_messages(messages, room_id, skip_sid=None):
    """ Inform other clients in room to delete messages """
    await sio.emit("message_deleted", {
        "messages": messages,
        "room_id": room_id
    }, room=room_id, skip_sid=skip_sid)


async def _job_callback(messages):
    deleted = await delete_expired_messages(messages)

    for room_id, messages in deleted.items():
        await delete_client_messages(messages, room_id)


async def job_disappear_messages():
    # print("Job ran")  # TODO(medium)(SpeedFox198): Change to log
    await messages_queue.check_disappearing_messages(_job_callback)


# TODO(high)(SpeedFox198):
# edit frequency of running scheduler
# 3 different timings == 3 different queues
async def task_disappear_messages(scheduler):
    """ Task to run scheduled checking for disappearing of messages """
    scheduler.add_job(job_disappear_messages, "interval", seconds=5)
    scheduler.start()
