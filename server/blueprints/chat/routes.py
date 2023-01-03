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
async def upload_and_scan_file(data: RequestFile):
    file_id = await upload_file(data.file)
    file_hash = await get_file_analysis(file_id)
    score = await scan_file_hash(file_hash)
    return {"Score": score}
