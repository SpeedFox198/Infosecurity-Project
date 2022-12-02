import quart_auth
from hypercorn.asyncio import serve
from quart import Quart
from quart_cors import cors
from constants import ASYNC_MODE, CORS_ALLOWED_ORIGINS
from config import config
import socketio
import asyncio
from blueprints.api import api_bp
from blueprints.user import auth_bp
from server.models import AuthedUser

DEBUG = True
PORT = 5000

sio = socketio.AsyncServer(async_mode=ASYNC_MODE, cors_allowed_origins=CORS_ALLOWED_ORIGINS)
app = Quart(__name__)
app = cors(app)
sio_app = socketio.ASGIApp(sio, app)
auth_manager = quart_auth.AuthManager()
auth_manager.user_class = AuthedUser
auth_manager.init_app(app)
api_bp.register_blueprint(auth_bp)
app.register_blueprint(api_bp)
app.secret_key = "secret123"


@sio.event
async def test(sid, data):
    print(f"Received data: {data}")
    await sio.emit("response", {"data":f"We received: {data['data']}"}, to=sid)
    await sio.emit("response", {"data":f"Broadcast: {data['data']}"})


asyncio.run(serve(sio_app, config))
