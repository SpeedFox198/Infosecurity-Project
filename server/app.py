from datetime import timedelta

import quart_auth
import quart_rate_limiter
import socketio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from blueprints.api import api_bp
from blueprints.auth import auth_bp
from blueprints.chat import chat_bp, messages_queue, sio, sio_auth_manager, task_disappear_messages
from blueprints.device import device_bp
from blueprints.friend import friend_bp
from blueprints.group import group_bp
from blueprints.media import media_bp
from blueprints.user import user_bp
from blueprints.settings import settings_bp
from db_access.device import get_device
from itsdangerous import URLSafeTimedSerializer
from models import AuthedUser
from quart import Quart
from quart_auth import AuthManager, current_user, logout_user
from quart_cors import cors
from quart_schema import QuartSchema, RequestSchemaValidationError
from utils.logging import log_warning

scheduler = AsyncIOScheduler()
app = Quart(__name__)
app = cors(app, allow_credentials=True, allow_origin=["https://localhost", "https://127.0.0.1"])
QuartSchema(app)

rate_limiter = quart_rate_limiter.RateLimiter(
    app,
    default_limits=[quart_rate_limiter.RateLimit(15, timedelta(minutes=1))]
)

auth_manager = AuthManager()
auth_manager.user_class = AuthedUser
auth_manager.init_app(app)

sio_auth_manager.register_app(app)  # Registers app to SocketIO Auth Manager

api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(chat_bp)
api_bp.register_blueprint(media_bp)
api_bp.register_blueprint(device_bp)
api_bp.register_blueprint(user_bp)
api_bp.register_blueprint(friend_bp)
api_bp.register_blueprint(settings_bp)
api_bp.register_blueprint(group_bp)
app.register_blueprint(api_bp)

app.secret_key = "L7h5TRk5EHS_ouNHtodgJX4KIb4fDl-JOKCzFnsj_8A"
app.config["QUART_AUTH_SALT"] = "IwPsU_TTTM_kKqr_nQglx7qUKwW1lLpZqtoHN9sWTpc"
app.config["QUART_AUTH_DURATION"] = 60 * 24 * 60 * 60  # formatted as (days * hours * minutes * seconds)
app.config["ATTACHMENTS_PATH"] = "media/attachments"

app.config["url_serialiser"] = URLSafeTimedSerializer(app.secret_key)


@app.before_request
async def before_request():
    if not await current_user.is_authenticated:
        return

    valid_device = await get_device(await current_user.user_id, await current_user.device_id)

    if not valid_device:
        await log_warning(
            f"Access attempt was made with an invalid device by {await current_user.username or 'Non existing user'}"
        )
        logout_user()


@app.errorhandler(500)
async def server_error(*_):
    return {"message": "Internal server error"}, 500


@app.errorhandler(quart_rate_limiter.RateLimitExceeded)
async def rate_limit_exceeded(*_):
    return {"message": "Rate limit exceeded"}, 429


@app.errorhandler(404)
async def not_found(*_):
    return {"message": "Requested resource is not found"}, 404


@app.errorhandler(quart_auth.Unauthorized)
async def unauthorized(*_):
    return {"message": "Not authorized"}, 401


@app.errorhandler(RequestSchemaValidationError)
async def invalid_schema(*_):
    return {"message": "Invalid request"}, 400


@app.before_serving
async def startup():
    await messages_queue.init_from_db()
    await task_disappear_messages(scheduler)


@app.after_serving
async def finish():
    scheduler.shutdown()


# The SocketIO app
# (which redirects non-SocketIO requests to Quart app)
sio_app = socketio.ASGIApp(sio, app)
