from quart import Blueprint
from security_functions.virustotal import (
    upload_file,
    get_file_analysis,
    scan_file_hash,
    get_url_analysis,
    get_url_report
)
from quart_auth import (
    login_required,
)
from quart_schema import validate_request
from models.request_data import RequestFile

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


@chat_bp.post("/file_upload_and_scan")
@login_required
@validate_request(RequestFile)
async def upload_and_scan_file(file: RequestFile):
    file_id = upload_file(file)
    file_hash = get_file_analysis(file_id)
    score = scan_file_hash(file_hash)
    return {"Score": score}
