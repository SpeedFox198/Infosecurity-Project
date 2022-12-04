import socketio
import sqlalchemy as sa
from db_access.globals import async_session
from models import AuthedUser, LoginData, User

ASYNC_MODE = "asgi"
CORS_ALLOWED_ORIGINS = "https://localhost"

sio = socketio.AsyncServer(async_mode=ASYNC_MODE, cors_allowed_origins=CORS_ALLOWED_ORIGINS)


# @sio.event
# async def test(sid, data):
#     print(f"Received data: {data}")
#     await sio.emit("response", {"data":f"We received: {data['data']}"}, to=sid)
#     # await sio.emit("response", {"data":f"Broadcast: {data['data']}"})



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
@sio.event
async def begin_chat(sid, room_id):
    sio.enter_room(sid, room_id)

# @sio.event
# def exit_chat(sid):
#     sio.leave_room(sid, "chat_users")
