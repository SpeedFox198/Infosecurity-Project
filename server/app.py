import asyncio

import quart_auth
import socketio
from blueprints.api import api_bp
from blueprints.chat import sio
from blueprints.auth import auth_bp
from config import config
from hypercorn.asyncio import serve
from models import AuthedUser
from quart import Quart
from quart_cors import cors

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
app = Quart(__name__)
app = cors(app)


auth_manager = quart_auth.AuthManager()
auth_manager.user_class = AuthedUser
auth_manager.init_app(app)

api_bp.register_blueprint(auth_bp)
app.register_blueprint(api_bp)
app.secret_key = "secret123"


# Serve the SocketIO app
# (which redirects non-SocketIO requests to Quart app)
sio_app = socketio.ASGIApp(sio, app)
asyncio.run(serve(sio_app, config))
