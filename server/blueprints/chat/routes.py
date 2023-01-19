from quart import Blueprint, request
from security_functions.virustotal import (
    upload_file,
    get_file_analysis,
    scan_file_hash,
    get_url_analysis,
    get_url_report
)
from quart_auth import login_required
from quart_schema import validate_request

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


@chat_bp.post("/file_upload_and_scan")
@login_required
async def upload_and_scan_file():
    file = await request.files
    file_id = upload_file(file)
    file_hash = get_file_analysis(file_id)
    score = scan_file_hash(file_hash)
    print(score)
    return {"Score": score}
    # print("\n\n\n")
    # print(request)
    # x = await request.files
    # print("\n\n\n")
    # return "lol"
