import socketio
import sqlalchemy as sa
from db_access.globals import async_session
from models import Message
from utils import to_unix

ASYNC_MODE = "asgi"
CORS_ALLOWED_ORIGINS = "https://localhost"
MESSAGE_LOAD_NUMBER = 20  # Number of messages to load at once

sio = socketio.AsyncServer(async_mode=ASYNC_MODE, cors_allowed_origins=CORS_ALLOWED_ORIGINS)


# TODO(SpeedFox198): remove temp values
temp_rooms = [
    {"icon": "/default.png", "name": "Grp Chat", "room_id": "room_1"},
    {"icon": "/default.png", "name": "Grp Chat", "room_id": "room_2"},
    {"icon": "/galaxy.jpg", "name": "Grp Chat", "room_id": "room_3"},
    {"icon": "/favicon.svg", "name": "Grp Chat", "room_id": "room_4"}
]


# TODO(SpeedFox198): do authentication
@sio.event
async def connect(sid, environ, auth):
    """ Event when client connects to server """
    # print("connected:", sid)
    # Do authentication
    for room in temp_rooms:
        sio.enter_room(sid, room["room_id"])
    # print(f"{sid} joined: {sio.rooms(sid)}")

    # Send room_ids that client belongs to
    await sio.emit("rooms_joined", temp_rooms, to=sid)


@sio.event
async def disconnect(sid):
    """ Event when client disconnects from server """
    # TODO(SpeedFox198): change to log later
    # print("disconnected:", sid)


# TODO(SpeedFox198): authenticate and verify msg (user, and format)
@sio.event
async def send_message(sid, data):
    print(f"Received {data}")  # TODO(SpeedFox198): change to log later

    # Create message object
    message = Message(
        data["user_id"],
        data["room_id"],
        data["content"],
        data["reply_to"],
        data["type"]
    )

    # Insert object into database
    async with async_session() as session:
        async with session.begin():
            session.add(message)

    # Forward messages to other clients in same room
    await sio.emit("receive_message", {
        "message_id": message.message_id,
        "room_id": message.room_id,
        "user_id": message.user_id,
        "time": to_unix(message.time),
        "content": message.content,
    }, room=data["room_id"], skip_sid=sid)

    # Return timestamp and message_id to client
    await sio.emit("sent_success", {
        "message_id": message.message_id,
        "room_id": message.room_id,
        "temp_id": data["message_id"],
        "time": to_unix(message.time)
    }, to=sid)


# TODO(SpeedFox198): authenticate and verify msg (user, and format)
@sio.event
async def get_room_messages(sid, data):
    # print(f"Received {data}")  # TODO(SpeedFox198): change to log later
    room_id = data["room_id"]
    n = data["n"]
    extra = data["extra"]
    limit  = MESSAGE_LOAD_NUMBER
    offset = MESSAGE_LOAD_NUMBER * n + extra

    room_messages = ()  # Default room messages to empty tuple

    # Get room messsages from database
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

        results = (await session.execute(statement)).all()
        room_messages = [{
            "message_id": results[i].message_id,
            "user_id": results[i].user_id,
            "time": to_unix(results[i].time),
            "content": results[i].content,
            "type": results[i].type
        } for i in range(len(results)-1, -1, -1)]

    await sio.emit("receive_room_messages", {
        "room_id": room_id,
        "room_messages": room_messages
    }, to=sid)


# TODO(SpeedFox198): authenticate and verify msg (user, and format)
# ensure user is part of room and is admin
# ensure data in correct format, (length of data also?)
@sio.event
async def delete_messages(sid, data):
    print(f"Received {data}")  # TODO(SpeedFox198): change to log later

    messages = data["messages"]
    room_id = data["room_id"]

    # Delete messages from database (ensures that room_id is correct)
    async with async_session() as session:
        statement = sa.select(Message.message_id).where(
            (Message.message_id.in_(messages))
            & (Message.room_id == room_id)
        )
        x = (await session.execute(statement)).fetchall()

        statement = sa.delete(Message).where(Message.message_id.in_(messages))
        await session.execute(statement)

        await session.commit()

    # Tell other clients in same room to delete the same messages
    await sio.emit("message_deleted", messages, room=room_id)  # TODO(SpeedFox198): skip_sid=sid

#TODO(SpeedFox198): after deletion rmb to decrease extra count in svelte stores!
