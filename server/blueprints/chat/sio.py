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

tmp_msgs = {
    "room_1": [
        {"message_id": "a00", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675711, "content": "Lorem 1"},
        {"message_id": "a01", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675722, "content": "Lorem Ipsum 2"},
        {"message_id": "a02", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675733, "content": "Lorem Ipsum what 3"},
        {"message_id": "a03", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675744, "content": "Lorem Ipsum what did 4"},
        {"message_id": "a04", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675755, "content": "Lorem Ipsum what did you 5"},
        {"message_id": "a05", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675766, "content": "Lorem Ipsum what did you expect 6"},
        {"message_id": "a06", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675777, "content": "Lorem Ipsum what did you expect lmao 7"},
        {"message_id": "a07", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675788, "content": "Lorem Ipsum what did you expect lmao 8"},
        {"message_id": "a08", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675799, "content": "Lorem Ipsum what did you expect lmao 9"},
        {"message_id": "a09", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675800, "content": "Lorem Ipsum what did you expect lmao 10"},
        {"message_id": "a10", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675811, "content": "Lorem 11"},
        {"message_id": "a11", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675822, "content": "Lorem Ipsum 12"},
        {"message_id": "a12", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675833, "content": "Lorem Ipsum what 13"},
        {"message_id": "a13", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675844, "content": "Lorem Ipsum what did 14"},
        {"message_id": "a14", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675855, "content": "Lorem Ipsum what did you 15"},
        {"message_id": "a15", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675866, "content": "Lorem Ipsum what did you expect 16"},
        {"message_id": "a16", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675877, "content": "Lorem Ipsum what did you expect lmao 17"},
        {"message_id": "a17", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675888, "content": "Lorem Ipsum what did you expect lmao 18"},
        {"message_id": "a18", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675899, "content": "Lorem Ipsum what did you expect lmao 19"},
        {"message_id": "a19", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675911, "content": "room 111 content"},
    ],
    "room_2": [
        {"message_id": "a20", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675711, "content": "Lorem 1"},
        {"message_id": "a21", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675722, "content": "Lorem Ipsum 2"},
        {"message_id": "a22", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675733, "content": "Lorem Ipsum what 3"},
        {"message_id": "a23", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675744, "content": "Lorem Ipsum what did 4"},
        {"message_id": "a24", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675755, "content": "Lorem Ipsum what did you 5"},
        {"message_id": "a25", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675766, "content": "Lorem Ipsum what did you expect 6"},
        {"message_id": "a26", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675777, "content": "Lorem Ipsum what did you expect lmao 7"},
        {"message_id": "a27", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675788, "content": "Lorem Ipsum what did you expect lmao 8"},
        {"message_id": "a28", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675799, "content": "Lorem Ipsum what did you expect lmao 9"},
        {"message_id": "a29", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675800, "content": "Lorem Ipsum what did you expect lmao 10"},
        {"message_id": "a30", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675811, "content": "Lorem 11"},
        {"message_id": "a31", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675822, "content": "Lorem Ipsum 12"},
        {"message_id": "a32", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675833, "content": "Lorem Ipsum what 13"},
        {"message_id": "a33", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675844, "content": "Lorem Ipsum what did 14"},
        {"message_id": "a34", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675855, "content": "Lorem Ipsum what did you 15"},
        {"message_id": "a35", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675866, "content": "Lorem Ipsum what did you expect 16"},
        {"message_id": "a36", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675877, "content": "Lorem Ipsum what did you expect lmao 17"},
        {"message_id": "a37", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675888, "content": "Lorem Ipsum what did you expect lmao 18"},
        {"message_id": "a38", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675899, "content": "Lorem Ipsum what did you expect lmao 19"},
        {"message_id": "a39", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675911, "content": "room 222 content"},
    ],
    "room_3": [
        {"message_id": "a40", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675711, "content": "Lorem 1"},
        {"message_id": "a41", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675722, "content": "Lorem Ipsum 2"},
        {"message_id": "a42", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675733, "content": "Lorem Ipsum what 3"},
        {"message_id": "a43", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675744, "content": "Lorem Ipsum what did 4"},
        {"message_id": "a44", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675755, "content": "Lorem Ipsum what did you 5"},
        {"message_id": "a45", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675766, "content": "Lorem Ipsum what did you expect 6"},
        {"message_id": "a46", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675777, "content": "Lorem Ipsum what did you expect lmao 7"},
        {"message_id": "a47", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675788, "content": "Lorem Ipsum what did you expect lmao 8"},
        {"message_id": "a48", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675799, "content": "Lorem Ipsum what did you expect lmao 9"},
        {"message_id": "a49", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675800, "content": "Lorem Ipsum what did you expect lmao 10"},
        {"message_id": "a50", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675811, "content": "Lorem 11"},
        {"message_id": "a51", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675822, "content": "Lorem Ipsum 12"},
        {"message_id": "a52", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675833, "content": "Lorem Ipsum what 13"},
        {"message_id": "a53", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675844, "content": "Lorem Ipsum what did 14"},
        {"message_id": "a54", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675855, "content": "Lorem Ipsum what did you 15"},
        {"message_id": "a55", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675866, "content": "Lorem Ipsum what did you expect 16"},
        {"message_id": "a56", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675877, "content": "Lorem Ipsum what did you expect lmao 17"},
        {"message_id": "a57", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675888, "content": "Lorem Ipsum what did you expect lmao 18"},
        {"message_id": "a58", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675899, "content": "Lorem Ipsum what did you expect lmao 19"},
        {"message_id": "a59", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675911, "content": "room 333 content"},
    ],
    "room_4": [
        {"message_id": "a60", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675711, "content": "Lorem 1"},
        {"message_id": "a61", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675722, "content": "Lorem Ipsum 2"},
        {"message_id": "a62", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675733, "content": "Lorem Ipsum what 3"},
        {"message_id": "a63", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675744, "content": "Lorem Ipsum what did 4"},
        {"message_id": "a64", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675755, "content": "Lorem Ipsum what did you 5"},
        {"message_id": "a65", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675766, "content": "Lorem Ipsum what did you expect 6"},
        {"message_id": "a66", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675777, "content": "Lorem Ipsum what did you expect lmao 7"},
        {"message_id": "a67", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675788, "content": "Lorem Ipsum what did you expect lmao 8"},
        {"message_id": "a68", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675799, "content": "Lorem Ipsum what did you expect lmao 9"},
        {"message_id": "a69", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675800, "content": "Lorem Ipsum what did you expect lmao 10"},
        {"message_id": "a70", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675811, "content": "Lorem 11"},
        {"message_id": "a71", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675822, "content": "Lorem Ipsum 12"},
        {"message_id": "a72", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675833, "content": "Lorem Ipsum what 13"},
        {"message_id": "a73", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675844, "content": "Lorem Ipsum what did 14"},
        {"message_id": "a74", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675855, "content": "Lorem Ipsum what did you 15"},
        {"message_id": "a75", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675866, "content": "Lorem Ipsum what did you expect 16"},
        {"message_id": "a76", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675877, "content": "Lorem Ipsum what did you expect lmao 17"},
        {"message_id": "a77", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675888, "content": "Lorem Ipsum what did you expect lmao 18"},
        {"message_id": "a78", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675899, "content": "Lorem Ipsum what did you expect lmao 19"},
        {"message_id": "a79", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675911, "content": "room 4 content"},
    ],
    "room_5": [
        {"message_id": "a80", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675711, "content": "Lorem 1"},
        {"message_id": "a81", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675722, "content": "Lorem Ipsum 2"},
        {"message_id": "a82", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675733, "content": "Lorem Ipsum what 3"},
        {"message_id": "a83", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675744, "content": "Lorem Ipsum what did 4"},
        {"message_id": "a84", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675755, "content": "Lorem Ipsum what did you 5"},
        {"message_id": "a85", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675766, "content": "Lorem Ipsum what did you expect 6"},
        {"message_id": "a86", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675777, "content": "Lorem Ipsum what did you expect lmao 7"},
        {"message_id": "a87", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675788, "content": "Lorem Ipsum what did you expect lmao 8"},
        {"message_id": "a88", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675799, "content": "Lorem Ipsum what did you expect lmao 9"},
        {"message_id": "a89", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675800, "content": "Lorem Ipsum what did you expect lmao 10"},
        {"message_id": "a90", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675811, "content": "Lorem 11"},
        {"message_id": "a91", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675822, "content": "Lorem Ipsum 12"},
        {"message_id": "a92", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675833, "content": "Lorem Ipsum what 13"},
        {"message_id": "a93", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675844, "content": "Lorem Ipsum what did 14"},
        {"message_id": "a94", "user_id": "427168ff-b76d-40f8-8111-e98cab5fe1f7", "time": 1670675855, "content": "Lorem Ipsum what did you 15"},
        {"message_id": "a95", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675866, "content": "Lorem Ipsum what did you expect 16"},
        {"message_id": "a96", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675877, "content": "Lorem Ipsum what did you expect lmao 17"},
        {"message_id": "a97", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675888, "content": "Lorem Ipsum what did you expect lmao 18"},
        {"message_id": "a98", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675899, "content": "Lorem Ipsum what did you expect lmao 19"},
        {"message_id": "a99", "user_id": "c5b87c16-f61d-4782-a709-6e3e18f5af5c", "time": 1670675911, "content": "room 5 content"},
    ],
}

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
    # TODO(SpeedFox198): remove if unused
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


@sio.event
async def get_room_messages(sid, data):
    # print(f"Received {data}")  # TODO(SpeedFox198): change to log later
    room_id = data["room_id"]
    n = data["n"]
    limit  = MESSAGE_LOAD_NUMBER
    offset = MESSAGE_LOAD_NUMBER * n

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
