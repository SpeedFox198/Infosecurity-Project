from quart import Blueprint, request
from security_functions.virustotal import (
    upload_file,
    get_file_analysis,
    scan_file_hash,
    get_url_analysis,
    get_url_report
)
from quart_auth import login_required, current_user
from quart_schema import validate_request

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


@chat_bp.post("/file_upload_and_scan")
@login_required
async def scan_file(file_hash):
    # function receives file hash and sent to virustotal for scanning

    
    score = scan_file_hash(file_hash)
    print(score)

    return {"Score": score}