import asyncio

import quart_auth
import socketio
from blueprints.api import api_bp
from blueprints.auth import auth_bp
from blueprints.chat import sio
from blueprints.device import device_bp
from blueprints.user import user_bp
from models import AuthedUser
from quart import Quart
from quart_cors import cors

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
app = Quart(__name__)
app = cors(app, allow_credentials=True, allow_origin=["https://localhost"])


auth_manager = quart_auth.AuthManager()
auth_manager.user_class = AuthedUser
auth_manager.init_app(app)

api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(user_bp)
api_bp.register_blueprint(device_bp)
app.register_blueprint(api_bp)
app.secret_key = "secret123"


@app.errorhandler(quart_auth.Unauthorized)
async def unauthorized(*_):
    return {"message": "Not authorized"}, 401


# The SocketIO app
# (which redirects non-SocketIO requests to Quart app)
sio_app = socketio.ASGIApp(sio, app)
