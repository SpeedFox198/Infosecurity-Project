import socketio
import sqlalchemy as sa
from db_access.globals import async_session
from models import AuthedUser, LoginData, User


ASYNC_MODE = "asgi"
CORS_ALLOWED_ORIGINS = "https://localhost"

sio = socketio.AsyncServer(async_mode=ASYNC_MODE, cors_allowed_origins=CORS_ALLOWED_ORIGINS)


# TODO(SpeedFox198): remove temp values
temp_rooms = [
    "room_1",
    "room_2",
    "room_3",
    "room_4",
    "room_5"
]

# TODO(SpeedFox198): do authentication
@sio.event()
async def connect(sid, environ, auth):
    print("connected:", sid)
    # Do authentication
    for room_id in temp_rooms:
        sio.enter_room(sid, room_id)
    print(f"{sid} joined: {sio.rooms(sid)}")

    # Send room_ids that client belongs to
    await sio.emit("rooms_joined", temp_rooms, to=sid)


@sio.event
async def send_message(sid, data):
    print(f"Received {data}")  # TODO(SpeedFox198): change to log later
    room = data["room_id"]
    # TODO(SpeedFox198): get username, avatar using user_id
    # Get time using pythong maybe?
    # Change format to getting those using another api
    await sio.emit("receive_message", {
        "room_id": room,
        "username": "<username>",
        "avatar": "/default.png",
        "time": "99:99PM",
        "content": data["content"],
    }, room=room, skip_sid=sid)
    # await sio.emit("sent_success", data, to=sid)


# TODO(SpeedFox198): add authentication and authorisation here
# LOGIC HAS CHANGED!
# When user connects to server, on the server side
# server will go into database and join user into every room
# that user belongs to!!!
# This solves a few issues:
# 1. Users will get real time updates of receiving msgs from any room
# 2. Client side won't be able to emit even to request for join room
# 3. Client side does not need to sort of maintain a list of room_id :)
@sio.event
async def join_room(sid, room_id):
    sio.enter_room(sid, room_id)

# @sio.event
# def exit_chat(sid):
#     sio.leave_room(sid, "chat_users")
