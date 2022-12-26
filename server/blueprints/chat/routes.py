from quart import Blueprint
from security_functions.virustotal import upload_file, get_file_analysis, scan_file_hash, get
from quart_auth import (
    login_required,
)

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

@chat_bp.post("/scan")
@login_required
async def upload_file(file):