import os

import socketio
import sqlalchemy as sa
from db_access.block import (db_check_block, db_create_block_entry,
                             db_delete_block_entry, db_get_blocked)
from db_access.globals import async_session
from db_access.message import (db_get_room_id_of_message, db_get_room_messages,
                               db_remove_messages, set_message_as_malicious,
                               set_messages_as_received)
from db_access.room import db_get_room_if_user_verified, db_update_disappearing, db_check_and_set_room_encrypted
from db_access.sio import (add_sio_connection, get_existing_room,
                           get_sids_from_sio_connection, has_disappearing,
                           have_e2ee_enabled, have_relationship,
                           remove_friend_request, remove_sio_connection,
                           set_online_status)
from db_access.user import get_user_details, db_enable_user_e2ee
from models import (AuthedUser, Friend, FriendRequest, Group, Membership,
                    Message, MessageStatus, Room)
from models.error import VirusTotalError
from models.request_data import GroupMetadataBody, ScanURLBody
from models.response_data import URLResultData
from pydantic import ValidationError
from security_functions.ocr import ocr_scan
from security_functions.virustotal import (get_file_analysis, get_url_analysis,
                                           get_url_report, scan_file_hash,
                                           upload_file, upload_url)
from socketio.exceptions import ConnectionRefusedError
from utils import remove_tree_directory, to_unix
from utils.logging import log_warning, log_exception

from .events import *
from .functions import (delete_expired_messages, get_room, messages_queue_5s,
                        messages_queue_7d, messages_queue_15s,
                        messages_queue_24h, messages_queue_30d, save_file,
                        save_group_icon)
from .sio_auth_manager import SioAuthManager
from .sio_redis_manager import SioRedisManager

ASYNC_MODE = "asgi"
CORS_ALLOWED_ORIGINS = "https://localhost"
MAX_HTTP_BUFFER_SIZE = 5000000  # 5 megabyte payload limit
SIO_SESSION_USER_KEY = "user"
MESSAGE_LOAD_NUMBER = 20  # Number of messages to load at once


mgr = SioRedisManager("redis://SocketIOServer:nOF1w!n35QCm1C3M7YfW3u_fIyuI0x~eg77H-SXJtByYWl!x4uSCUuP@redis-18687.c263.us-east-1-2.ec2.cloud.redislabs.com:18687")
sio = socketio.AsyncServer(
    async_mode=ASYNC_MODE,
    cors_allowed_origins=CORS_ALLOWED_ORIGINS,
    max_http_buffer_size=MAX_HTTP_BUFFER_SIZE,
    client_manager=mgr
)

sio_auth_manager = SioAuthManager()  # Authentication Manager


# TODO(medium)(SpeedFox198): logging
@sio.event
async def connect(sid, environ, auth):
    """ Event when client connects to server """
    current_user = sio_auth_manager.get_user(environ["HTTP_COOKIE"])
    current_user_id = await current_user.user_id

    # Check if user_id is valid in database, because there was an integrity error when re-init db
    if await get_user_details(current_user_id) is None:
        raise ConnectionRefusedError("Authentication failed")

    if not await current_user.is_authenticated:
        raise ConnectionRefusedError("Authentication failed")

    # Save user session
    await save_user(sid, current_user)

    await set_online_status(current_user_id, True)
    await add_sio_connection(sid, current_user_id)

    # Add client to their respective rooms
    rooms = await get_room(current_user_id)
    blocked = await db_get_blocked(current_user_id)

    enter_room(sid, current_user_id)

    for room in rooms:
        room_id = room["room_id"]

        # Check if chat (user) is being blocked
        room_is_blocked = False
        for blocked_room in blocked:
            if room_id == blocked_room.room_id:
                blocked_status = "blocking" if current_user_id == blocked_room.user_id else "blocked"
                room["blocked"] = blocked_status
                room["online"] = False
                room_is_blocked = True
                break

        # Do not enter user into rooms that are blocked
        if room_is_blocked:
            continue

        enter_room(sid, room_id)

        # Inform other online users that current user is online
        # Only emit event to direct messages rooms
        if room["type"] == "direct":
            await sio.emit(USER_ONLINE, {"user_id": current_user_id}, to=room_id)

    # Send room_ids that client belongs to
    await sio.emit(ROOMS_JOINED, rooms, to=sid)


@sio.event
async def disconnect(sid):
    """ Event when client disconnects from server """
    # TODO(medium)(SpeedFox198): change to log later
    # print("disconnected:", sid)
    current_user = await get_user(sid)
    current_user_id = await current_user.user_id

    await remove_sio_connection(sid, current_user_id)

    # Only proceed to make user offline if user has 0 sio connection
    if await get_sids_from_sio_connection(current_user_id):
        return

    await set_online_status(current_user_id, False)

    # ignore the fact that we emit event to all rooms including groups
    # cuz we running out of time
    for room_id in sio.rooms(sid):
        await sio.emit(USER_OFFLINE, {"user_id": current_user_id}, to=room_id)


# TODO(medium)(SpeedFox198): authenticate and verify msg (and format)
@sio.event
async def send_message(sid: str, data: dict):
    # print(f"Received {data}")  # TODO(medium)(SpeedFox198): change to log later

    message_data = data["message"]
    file = data.get("file", None)
    filename = data.get("filename", "")
    height = width = None  # Initialise height and width values

    # Get user from session
    user = await get_user(sid)
    user_id = await user.user_id

    # Get room
    room = await db_get_room_if_user_verified(message_data["room_id"], user_id)
    if room is None:  # If room not found, abort adding of message
        return

    # If room is blocked, block sending of message
    if await db_check_block(room.room_id):
        # TODO(high)(SpeedFox198): handle event on client side
        await sio.emit(MESSAGE_BLOCKED, {"temp_id": message_data["message_id"]}, to=sid)
        return

    # Insert object into database
    async with async_session() as session:

        # Create message object
        message = Message(
            user_id,
            room.room_id,
            message_data["content"],
            reply_to=message_data["reply_to"],  # TODO(low)(SpeedFox198): remove if unused
            type_=message_data["type"],
            encrypted=room.encrypted
        )

        message.status = MessageStatus(message.message_id, message.room_id)

        # Add message to database
        async with session.begin():
            session.add(message)

        # Save file if message type is not text, and file exists
        # TODO(high)(SpeedFox198): test what happens when upload file of size 0 bytes lmao
        if message.type != "text" and file:
            filename, height, width = await save_file(
                sio_auth_manager.app.config["ATTACHMENTS_PATH"],
                file, filename, message.room_id, message.message_id, session
            )

    # If room has disappearing messages enabled
    # TODO(low)(SpeedFox198): remove demo values
    if room.disappearing == "5s":
        await messages_queue_5s.add_disappearing_messages(message.message_id)
    elif room.disappearing == "15s":
        await messages_queue_15s.add_disappearing_messages(message.message_id)
    elif room.disappearing == "24h":
        await messages_queue_24h.add_disappearing_messages(message.message_id)
    elif room.disappearing == "7d":
        await messages_queue_7d.add_disappearing_messages(message.message_id)
    elif room.disappearing == "30d":
        await messages_queue_30d.add_disappearing_messages(message.message_id)

    # Forward messages to other clients in same room
    await sio.emit(RECEIVE_MESSAGE, {
        "message_id": message.message_id,
        "room_id": message.room_id,
        "user_id": message.user_id,
        "time": to_unix(message.time),
        "content": message.content,
        "encrypted": message.encrypted,
        "type": message.type,
        "received": message.status.received,
        "malicious": message.status.malicious
    }, room=message_data["room_id"], skip_sid=sid)

    # Return timestamp and message_id to client
    data = {
        "message_id": message.message_id,
        "room_id": message.room_id,
        "temp_id": message_data["message_id"],
        "time": to_unix(message.time),
        "filename": filename,
        "encrypted": message.encrypted
    }
    if height and width:
        data["height"] = height
        data["width"] = width
    await sio.emit(SENT_SUCCESS, data, to=sid)

    # Check virus total if file attached and message not e2ee
    if message.type != "text" and file and not message.encrypted:
        file_id = await upload_file(file)
        file_hash = await get_file_analysis(file_id)
        await check_malicious_file(file_hash, message.message_id)


# TODO(medium)(SpeedFox198): authenticate and verify msg (and format)
@sio.event
async def get_room_messages(sid: str, data: dict):
    # print(f"Received {data}")  # TODO(medium)(SpeedFox198): change to log later
    room_id = data["room_id"]
    n = data["n"]
    extra = data["extra"]
    limit = MESSAGE_LOAD_NUMBER
    offset = MESSAGE_LOAD_NUMBER * n + extra

    # Get room messages from database
    room_messages = await db_get_room_messages(room_id, limit, offset)

    await sio.emit(RECEIVE_ROOM_MESSAGES, {
        "room_id": room_id,
        "room_messages": room_messages
    }, to=sid)


@sio.event
async def messages_received(sid: str, data: dict):
    received: list[str] = data.get("messages")

    if not received:
        return

    await set_messages_as_received(received)


# TODO(medium)(SpeedFox198): delete media if exists
# TODO(medium)(SpeedFox198): authenticate and verify msg (and format)
# ensure user is part of room and is admin
# ensure data in correct format, (length of data also?)
@sio.event
async def delete_messages(sid: str, data: dict):
    # print(f"Received {data}")  # TODO(medium)(SpeedFox198): change to log later

    messages = data["messages"]
    room_id = data["room_id"]

    # Get user from session
    user = await get_user(sid)
    user_id = await user.user_id

    # Delete messages from room with the appropriate permissions of user
    messages = await db_remove_messages(messages, room_id, user_id)

    # Tell other clients in same room to delete the same messages
    await delete_client_messages(messages, room_id)
    # TODO(UI)(SpeedFox198): skip_sid=sid (client side must del 1st)
    # ^ maybe not? (im lazy)


@sio.event
async def create_group(sid: str, data: dict):
    current_user = await get_user(sid)
    have_group_icon = False
    icon_path = None

    try:
        group_metadata = GroupMetadataBody(**data)
    except ValidationError as err:
        await log_exception(err)
        error_list = [error["msg"] for error in err.errors()]
        error_message = error_list[0]
        await sio.emit(CREATE_GROUP_ERROR, {
            "message": error_message
        }, to=sid)
        return

    new_room = Room(group_metadata.disappearing, type_="group")

    if group_metadata.icon and group_metadata.icon_name:
        icon_path = await save_group_icon(new_room.room_id, group_metadata.icon_name, group_metadata.icon)
        is_image_sensitive = ocr_scan(icon_path)
        if is_image_sensitive:
            await remove_tree_directory(os.path.dirname(icon_path))
            await log_warning(
                f"User {await current_user.username} tried to upload a sensitive image when creating group"
            )
            await sio.emit(CREATE_GROUP_ERROR, {
                "message": "Group icon contains sensitive data"
            })
            return
        have_group_icon = True

    async with async_session() as session:
        # Create new room
        session.add(new_room)
        await session.flush()

        if have_group_icon:
            # Add Group icon if any and the group details
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

    await sio.emit(GROUP_CREATED, to=sid)

    # Emit event to update users they have been added to group
    for user_id in (group_metadata.users + [await current_user.user_id]):
        user_sids = await get_sids_from_sio_connection(user_id)
        if not user_sids:
            continue

        rooms = await get_room(user_id)
        for user_sid in user_sids:
            for room in rooms:
                if enter_room(user_sid, room["room_id"]):
                    continue

            # Send room_ids that client belongs to
            await sio.emit(GROUP_INVITE, rooms, to=user_sid)


@sio.event
async def send_friend_request(sid: str, data: dict):
    current_user = await get_user(sid)
    recipient_id = data.get("user")
    if recipient_id is None:
        await sio.emit(FRIEND_REQUEST_FAILED, {
            "message": "Invalid user"
        }, to=sid)
        return

    valid_recipient = await get_user_details(recipient_id)
    if valid_recipient is None:
        await sio.emit(FRIEND_REQUEST_FAILED, {
            "message": "Invalid user"
        }, to=sid)
        return

    possible_relationship = (await current_user.user_id, recipient_id)
    existing_friend = await have_relationship(possible_relationship)
    if existing_friend:
        await sio.emit(FRIEND_REQUEST_FAILED, {
            "message": "Cannot add an existing friend"
        }, to=sid)
        return

    async with async_session() as session:
        fr_made_before_statement = sa.select(FriendRequest).where(
            (FriendRequest.sender == await current_user.user_id) &
            (FriendRequest.recipient == recipient_id)
        )
        friend_request_made_before: FriendRequest | None = (await session.execute(fr_made_before_statement)).first()
        if friend_request_made_before:
            await sio.emit(FRIEND_REQUEST_FAILED, {
                "message": "Request was sent previously"
            }, to=sid)
            return

        session.add(
            FriendRequest(sender=await current_user.user_id,
                          recipient=recipient_id)
        )
        await session.commit()

    await sio.emit(FRIEND_REQUEST_SENT, data=recipient_id, to=sid)
    recipient_sids = await get_sids_from_sio_connection(recipient_id)
    for recipient_sid in recipient_sids:
        await sio.emit(FRIEND_REQUESTS_UPDATE, to=recipient_sid)


@sio.event
async def cancel_sent_friend_request(sid: str, data: dict):
    current_user = await get_user(sid)

    recipient_id = data.get("user")
    if recipient_id is None:
        await sio.emit(FAILED_CANCEL_FRIEND_REQUEST, {
            "message": "Invalid user"
        }, to=sid)
        return

    valid_recipient = await get_user_details(recipient_id)
    if valid_recipient is None:
        await sio.emit(FAILED_CANCEL_FRIEND_REQUEST, {
            "message": "Invalid user"
        }, to=sid)
        return

    await remove_friend_request(await current_user.user_id, recipient_id)
    await sio.emit(FRIEND_REQUESTS_UPDATE, data=recipient_id, to=sid)

    recipient_sids = await get_sids_from_sio_connection(recipient_id)
    for recipient_sid in recipient_sids:
        await sio.emit(FRIEND_REQUESTS_UPDATE, data=recipient_id, to=recipient_sid)


@sio.event
async def accept_friend_request(sid: str, data: dict):
    current_user = await get_user(sid)

    sender_id = data.get("user")
    if sender_id is None:
        await sio.emit(FAILED_ACCEPT_FRIEND_REQUEST, {
            "message": "Invalid user"
        }, to=sid)
        return

    valid_sender = await get_user_details(sender_id)
    if valid_sender is None:
        await sio.emit(FAILED_ACCEPT_FRIEND_REQUEST, {
            "message": "Invalid user"
        }, to=sid)
        return

    await remove_friend_request(sender_id, await current_user.user_id)
    async with async_session() as session:
        session.add(Friend(sender_id, await current_user.user_id))
        await session.commit()

    await sio.emit(FRIEND_REQUESTS_UPDATE, to=sid)

    sender_sids = await get_sids_from_sio_connection(sender_id)
    for sender_sid in sender_sids:
        await sio.emit(FRIEND_REQUESTS_UPDATE, to=sender_sid)


@sio.event
async def cancel_received_friend_request(sid: str, data: dict):
    current_user = await get_user(sid)

    sender_id = data.get("user")
    if sender_id is None:
        await sio.emit(FAILED_ACCEPT_FRIEND_REQUEST, {
            "message": "Invalid user"
        }, to=sid)
        return

    valid_sender = await get_user_details(sender_id)
    if valid_sender is None:
        await sio.emit(FAILED_ACCEPT_FRIEND_REQUEST, {
            "message": "Invalid user"
        }, to=sid)
        return

    await remove_friend_request(sender_id, await current_user.user_id)
    await sio.emit(FRIEND_REQUESTS_UPDATE, to=sid)

    sender_sids = await get_sids_from_sio_connection(sender_id)
    for sender_sid in sender_sids:
        await sio.emit(FRIEND_REQUESTS_UPDATE, to=sender_sid)


@sio.event
async def remove_friend(sid: str, data: dict):
    current_user = await get_user(sid)

    friend_user_id: str = data.get("user")
    if friend_user_id is None:
        await sio.emit(REMOVE_FRIEND_FAILED, {
            "message": "Invalid user"
        }, to=sid)
        return

    relationship = (await current_user.user_id, friend_user_id)

    valid_friend = await have_relationship(relationship)
    if not valid_friend:
        await sio.emit(REMOVE_FRIEND_FAILED, {
            "message": "Invalid friend"
        }, to=sid)
        return

    async with async_session() as session:
        statement = sa.delete(Friend).where(
            Friend.user1_id.in_(relationship) &
            Friend.user2_id.in_(relationship)
        )
        await session.execute(statement)
        await session.commit()

    await sio.emit(FRIEND_REMOVED, to=sid)
    ex_friend_sids = await get_sids_from_sio_connection(friend_user_id)
    for ex_friend_sid in ex_friend_sids:
        await sio.emit(FRIEND_REMOVED, to=ex_friend_sid)


@sio.event
async def message_friend(sid: str, data: dict):
    friend_user_id: str | None = data.get("user")
    if friend_user_id is None:
        await sio.emit(MESSAGE_FRIEND_ERROR, {
            "message": "Invalid user"
        }, to=sid)

    current_user = await get_user(sid)
    relationship = (await current_user.user_id, friend_user_id)

    valid_friend = await have_relationship(relationship)
    if not valid_friend:
        await sio.emit(MESSAGE_FRIEND_ERROR, {
            "message": "Invalid friend"
        }, to=sid)
        return

    existing_private_room = await get_existing_room(relationship)
    if existing_private_room:
        await sio.emit(MESSAGE_FRIEND_ERROR, {
            "message": "Message with selected friend already exists"
        }, to=sid)
        return

    async with async_session() as session:
        default_disappearing_option = "30d"

        if (await have_e2ee_enabled(await current_user.user_id)) and (await have_e2ee_enabled(friend_user_id)):
            new_room = Room(disappearing="off", encrypted=True)
        else:
            new_room = Room(disappearing="off")

        if await current_user.disappearing and await has_disappearing(friend_user_id):
            new_room.disappearing = default_disappearing_option

        session.add(new_room)
        await session.flush()

        session.add(Membership(new_room.room_id, await current_user.user_id, is_admin=True))
        await session.flush()
        session.add(Membership(new_room.room_id, friend_user_id, is_admin=True))
        await session.flush()

        await session.commit()

    await sio.emit(MESSAGE_FRIEND_SUCCESS, to=sid)

    for user_id in relationship:
        user_sids = await get_sids_from_sio_connection(user_id)
        if not user_sids:
            continue

        rooms = await get_room(user_id)

        for user_sid in user_sids:
            if enter_room(user_sid, new_room.room_id):
                continue
            await sio.emit(ROOMS_JOINED, rooms, to=user_sid)


@sio.event
async def set_disappearing(sid: str, data: dict):
    disappearing = data["disappearing"]
    room_id = data["room_id"]

    # Get user from session
    current_user = await get_user(sid)
    user_id = await current_user.user_id

    rooms = await get_room(user_id)

    exists = False
    for room in rooms:
        if (
                room_id == room["room_id"] and
                (room["type"] == "direct" or room["is_admin"] == True)
        ):
            exists = True
            room["disappearing"] = disappearing
            break

    if not exists:
        return

    await db_update_disappearing(disappearing, room_id)

    # Send room_ids that client belongs to
    await sio.emit(UPDATE_DISAPPEARING, {"room_id": room_id, "disappearing": disappearing}, room=room_id)


@sio.event
async def scan_hash(sid: str, data: dict):
    file_hash = data.get("hash", "")
    message_id = data.get("message_id", "")

    # TODO(low) screw this (disallow multple on same file idk)
    await check_malicious_file(file_hash, message_id)


@sio.event
async def block_user(sid: str, data: dict):
    block_id = data["block_id"]
    room_id = data["room_id"]

    # Get user from session
    current_user = await get_user(sid)
    current_user_id = await current_user.user_id

    # Block user (database)
    blocked_success = await db_create_block_entry(current_user_id, block_id, room_id)
    if not blocked_success:
        return

    # Offline user from blocked user
    blocked_user_sids = await get_sids_from_sio_connection(block_id)
    current_user_sids = await get_sids_from_sio_connection(current_user_id)

    for blocked_user_sid in blocked_user_sids:
        await sio.emit(USER_OFFLINE, {"user_id": current_user_id}, to=blocked_user_sid)

    for current_user_sid in current_user_sids:
        await sio.emit(USER_OFFLINE, {"user_id": block_id}, to=current_user_sid)

    # Update user blocked status
    await sio.emit(ROOM_BLOCKED, {"room_id": room_id, "block_id": block_id}, room=room_id)
    await sio.close_room(room_id)


@sio.event
async def unblock_user(sid: str, data: dict):
    block_id = data["block_id"]
    room_id = data["room_id"]

    # Get user from session
    current_user = await get_user(sid)
    current_user_id = await current_user.user_id

    # Block user (database)
    blocked_success = await db_delete_block_entry(current_user_id, block_id, room_id)
    if not blocked_success:
        return

    # Online user from blocked user
    blocked_user_sids = await get_sids_from_sio_connection(block_id)
    current_user_sids = await get_sids_from_sio_connection(current_user_id)

    for blocked_user_sid in blocked_user_sids:
        await sio.emit(USER_ONLINE, {"user_id": current_user_id}, to=blocked_user_sid)
        enter_room(blocked_user_sid, room_id)

    blocked_user_is_online = len(blocked_user_sids) > 0
    for current_user_sid in current_user_sids:
        if blocked_user_is_online:
            await sio.emit(USER_ONLINE, {"user_id": block_id}, to=current_user_sid)
        enter_room(current_user_sid, room_id)

    # Update user blocked status
    await sio.emit(ROOM_UNBLOCKED, {"room_id": room_id}, room=room_id)


@sio.event
async def enable_e2ee(sid: str):
    current_user = await get_user(sid)
    current_user_id = await current_user.user_id

    await db_enable_user_e2ee(current_user_id)
    room_ids = await db_check_and_set_room_encrypted(current_user_id)

    for room_id in room_ids:
        await sio.emit(ROOM_ENCRYPTED, {"room_id": room_id}, room=room_id)

    await sio.emit(E2EE_ENABLED, room=current_user_id)


@sio.event
async def check_safe_url(sid: str, data: dict):
    try:
        url_request = ScanURLBody(**data)
    except ValidationError as err:
        await log_exception(err)
        return

    is_malicious = False

    for url in url_request.urls:
        try:
            data_id = await upload_url(url)
            url_id = await get_url_analysis(data_id)
            results = URLResultData(**await get_url_report(url_id))
        except VirusTotalError as err:
            await log_exception(err)
            return

        if results.malicious > 0 or results.suspicious > 0:
            is_malicious = True
            await set_message_as_malicious(url_request.message_id)
            await log_warning(
                f"Message {url_request.message_id} detected to have malicious URL(s)"
            )
            break

    room_origin = await db_get_room_id_of_message(url_request.message_id)

    await sio.emit("malicious_check", {
        "message_id": url_request.message_id,
        "malicious": is_malicious
    }, room=room_origin)


async def save_user(sid: str, user: AuthedUser) -> None:
    """ Save user object to sio session """
    await sio.save_session(sid, {SIO_SESSION_USER_KEY: user})


async def get_user(sid: str) -> AuthedUser | None:
    """ Returns user object from sio session """
    return (await sio.get_session(sid)).get(SIO_SESSION_USER_KEY, None)


def enter_room(sid: str, room: str) -> bool:
    """ Attempts to enter sid into room, returns True if failed to enter """
    try:
        sio.enter_room(sid, room)
    except KeyError:
        return True
    return False


async def delete_client_messages(messages, room_id, skip_sid=None):
    """ Inform other clients in room to delete messages """
    await sio.emit(MESSAGE_DELETED, {
        "messages": messages,
        "room_id": room_id
    }, room=room_id, skip_sid=skip_sid)


async def check_malicious_file(file_hash, message_id):
    # Setting malicious flag to false
    malicious = False

    # scan file hash with virustotal
    score = await scan_file_hash(file_hash)
    if score > 0:
        malicious = True
        await set_message_as_malicious(message_id)
        await log_warning(
            f"Message {message_id} is detected to have a malicious file."
        )

    room_id = await db_get_room_id_of_message(message_id)

    await sio.emit("malicious_check", {"message_id": message_id, "malicious": malicious}, room=room_id)


async def _job_callback(messages):
    deleted = await delete_expired_messages(messages)

    for room_id, messages in deleted.items():
        await delete_client_messages(messages, room_id)


async def job_disappear_messages_5s():
    await messages_queue_5s.check_disappearing_messages(_job_callback)


async def job_disappear_messages_15s():
    await messages_queue_15s.check_disappearing_messages(_job_callback)


async def job_disappear_messages_24h():
    await messages_queue_24h.check_disappearing_messages(_job_callback)


async def job_disappear_messages_7d():
    await messages_queue_7d.check_disappearing_messages(_job_callback)


async def job_disappear_messages_30d():
    await messages_queue_30d.check_disappearing_messages(_job_callback)


# TODO(high)(SpeedFox198):
# edit frequency of running scheduler
# 3 different timings == 3 different queues
async def task_disappear_messages(scheduler):
    """ Task to run scheduled checking for disappearing of messages """
    scheduler.add_job(job_disappear_messages_5s, "interval", seconds=3)
    scheduler.add_job(job_disappear_messages_15s, "interval", seconds=5)
    scheduler.add_job(job_disappear_messages_24h, "interval", hours=2)
    scheduler.add_job(job_disappear_messages_7d, "interval", hours=4)
    scheduler.add_job(job_disappear_messages_30d, "interval", hours=6)
    scheduler.start()
