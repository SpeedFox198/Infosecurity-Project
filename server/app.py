import asyncio

import quart_auth
import socketio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from blueprints.api import api_bp
from blueprints.auth import auth_bp
from blueprints.chat import job_disappear_messages, sio
from blueprints.device import device_bp
from blueprints.user import user_bp
from db_access.device import get_device
from models import AuthedUser
from quart import Quart
from quart_auth import AuthManager, current_user, logout_user
from quart_cors import cors
from quart_schema import QuartSchema, RequestSchemaValidationError
from utils.logging import log_warning


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
app = Quart(__name__)
app = cors(app, allow_credentials=True, allow_origin=["https://localhost"])
QuartSchema(app)


auth_manager = AuthManager()
auth_manager.user_class = AuthedUser
auth_manager.init_app(app)

api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(user_bp)
api_bp.register_blueprint(device_bp)
app.register_blueprint(api_bp)
app.secret_key = "secret123"


@app.before_request
async def before_request():
    if not await current_user.is_authenticated:
        return

    valid_device = await get_device(await current_user.user_id, await current_user.device_id)

    if not valid_device:
        await log_warning(
            f"Access attempt was made with an invalid device by {await current_user.username}"
        )
        logout_user()


@app.errorhandler(quart_auth.Unauthorized)
async def unauthorized(*_):
    return {"message": "Not authorized"}, 401


@app.errorhandler(RequestSchemaValidationError)
async def invalid_schema(*_):
    return {"message": "Invalid request"}, 400


async def task_disappear_messages():
    """ Task to run scheduled checking for disappearing of messages """
    global scheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(job_disappear_messages, "interval", seconds=1)
    scheduler.start()


@app.before_serving
async def startup():
    loop = asyncio.get_event_loop()
    loop.create_task(task_disappear_messages())


@app.after_serving
async def finish():
    scheduler.shutdown()


# The SocketIO app
# (which redirects non-SocketIO requests to Quart app)
sio_app = socketio.ASGIApp(sio, app)
