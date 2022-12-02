from hypercorn.config import Config
from hypercorn.asyncio import serve
from quart import Quart
from quart_cors import cors
from functools import wraps
from constants import ASYNC_MODE, CORS_ALLOWED_ORIGINS
from config import config
import socketio
import asyncio

DEBUG = True
PORT = 5000

sio = socketio.AsyncServer(async_mode=ASYNC_MODE, cors_allowed_origins=CORS_ALLOWED_ORIGINS)
app = Quart(__name__)
app = cors(app)
sio_app = socketio.ASGIApp(sio, app)

@sio.event
async def test(sid, data):
    print(f"Received data: {data}")
    await sio.emit("response", {"data":f"We received: {data['data']}"}, to=sid)
    # await sio.emit("response", {"data":f"Broadcast: {data['data']}"})



# app.run(debug=DEBUG, port=PORT)  # Run app
# config = Config.from_toml("server/config.toml")
asyncio.run(serve(sio_app, config))
