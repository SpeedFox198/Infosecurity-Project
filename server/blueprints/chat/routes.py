from db_access.user import set_user_public_key
from quart import Blueprint, request
from quart_auth import login_required, current_user
from quart_schema import validate_request

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


@chat_bp.post("/upload-public-key")
@login_required
async def scan_file():
    data = await request.get_json()
    public_key = data.get("public_key", "")
    user_id = await current_user.user_id
    await set_user_public_key(user_id, public_key)

    return { "message": "Public key uploaded" }
