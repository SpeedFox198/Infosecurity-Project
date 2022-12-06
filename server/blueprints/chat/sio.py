import socketio
import sqlalchemy as sa
from db_access.globals import async_session
from models import AuthedUser, LoginData, User


ASYNC_MODE = "asgi"
CORS_ALLOWED_ORIGINS = "https://localhost"

sio = socketio.AsyncServer(async_mode=ASYNC_MODE, cors_allowed_origins=CORS_ALLOWED_ORIGINS)


# TODO(SpeedFox198): remove temp values
temp_rooms = [
    {"icon":"/default.png", "name":"Grp Chat", "room_id":"room_1"},
    {"icon":"/default.png", "name":"Grp Chat", "room_id":"room_2"},
    {"icon":"/galaxy.jpg", "name":"Grp Chat", "room_id":"room_3"},
    {"icon":"/favicon.svg", "name":"Grp Chat", "room_id":"room_4"}
]

tmp_msgs = {
    "room_1": [
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem 1"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum 2"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what 3"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what did 4"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what did you 5"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect 6"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 7"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 8"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 9"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 10"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem 11"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum 12"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what 13"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what did 14"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what did you 15"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect 16"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 17"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 18"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 19"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"room 111 content"},
    ],
    "room_2": [
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem 1"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum 2"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what 3"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what did 4"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what did you 5"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect 6"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 7"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 8"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 9"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 10"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem 11"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum 12"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what 13"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what did 14"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what did you 15"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect 16"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 17"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 18"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 19"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"room 222 content"},
    ],
    "room_3": [
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem 1"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum 2"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what 3"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what did 4"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what did you 5"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect 6"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 7"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 8"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 9"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 10"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem 11"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum 12"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what 13"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what did 14"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what did you 15"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect 16"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 17"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 18"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 19"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"room 333 content"},
    ],
    "room_4": [
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem 1"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum 2"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what 3"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what did 4"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what did you 5"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect 6"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 7"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 8"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 9"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 10"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem 11"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum 12"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what 13"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what did 14"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what did you 15"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect 16"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 17"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 18"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 19"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"room 4 content"},
    ],
    "room_5": [
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem 1"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum 2"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what 3"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what did 4"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what did you 5"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect 6"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 7"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 8"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 9"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 10"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem 11"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum 12"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what 13"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what did 14"},
        {"user_id":"2a3f14df-ef17-4410-baf9-ed6693ac8c5a", "time":"99:99PM", "content":"Lorem Ipsum what did you 15"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect 16"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 17"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 18"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"Lorem Ipsum what did you expect lmao 19"},
        {"user_id":"ac4528d0-98f3-41a3-9516-03381f76c374", "time":"99:99PM", "content":"room 5 content"},
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
    # print("disconnected:", sid)


@sio.event
async def send_message(sid, data):
    print(f"Received {data}")  # TODO(SpeedFox198): change to log later
    # TODO(SpeedFox198):
    # Change temp things to actual
    # Get time using python maybe?
    # Change format to getting those using another api (<- ??? what was i refering to b4?)
    await sio.emit("receive_message", {
        "room_id": data["room_id"],
        "user_id": data["user_id"],
        "time": "99:99PM",
        "content": data["content"],
    }, room=data["room_id"], skip_sid=sid)

    # TODO(SpeedFox198): consider if you want sent receipt
    # await sio.emit("sent_success", data, to=sid)


@sio.event
async def get_room_messages(sid, data):
    # print(f"Received {data}")  # TODO(SpeedFox198): change to log later
    room_id = data["room_id"]
    room_messages = tmp_msgs[room_id]
    await sio.emit("receive_room_messages", {
        "room_id": room_id,
        "room_messages": room_messages
    }, to=sid)
