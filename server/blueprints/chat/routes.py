import socketio
import sqlalchemy as sa
from config import ASYNC_MODE, CORS_ALLOWED_ORIGINS
from db_access.globals import async_session
from models import AuthedUser, LoginData, User

sio = socketio.AsyncServer(async_mode=ASYNC_MODE, cors_allowed_origins=CORS_ALLOWED_ORIGINS)


@sio.event
async def test(sid, data):
    print(f"Received data: {data}")
    await sio.emit("response", {"data":f"We received: {data['data']}"}, to=sid)
    # await sio.emit("response", {"data":f"Broadcast: {data['data']}"})




@sio.event
async def send_message(sid, data):
    room = "<room>"  # Get room from data/database
    await sio.emit('my reply', data, room=room, skip_sid=sid)
