from db_access.user import db_set_user_public_key, db_set_user_wrap_key
from quart import Blueprint, request
from quart_auth import login_required, current_user
from quart_schema import validate_request
from models.request_data import WrapKeyBody

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


@chat_bp.post("/upload-public-key")
@login_required
async def upload_public_key():
    data = await request.get_json()
    public_key = data.get("public_key", "")
    user_id = await current_user.user_id
    await db_set_user_public_key(user_id, public_key)

    return { "message": "Public key uploaded" }


@chat_bp.post("/upload-wrap-key")
@login_required
@validate_request(WrapKeyBody)
async def upload_wrap_key(data: WrapKeyBody):
    user_id = await current_user.user_id
    await db_set_user_wrap_key(user_id, data.wrap_key)

    return { "message": "Wrap key uploaded" }
