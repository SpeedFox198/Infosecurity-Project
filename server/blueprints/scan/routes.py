from quart import Blueprint
from quart_auth import login_required
from quart_schema import validate_request

from models.error import VirusTotalError
from models.request_data import ScanURLBody
from models.response_data import URLResultData
from security_functions.virustotal import (
    upload_url,
    get_url_analysis,
    get_url_report
)

scan_bp = Blueprint("scan", __name__, url_prefix="/scan")


@scan_bp.post("/url")
@login_required
@validate_request(ScanURLBody)
async def scan_url(data: ScanURLBody):
    try:
        data_id = await upload_url(data.url)
        url_id = await get_url_analysis(data_id)
        results = URLResultData(**await get_url_report(url_id))
    except VirusTotalError as error:
        return {"message": str(error)}, 500

    if results.malicious > 0 or results.suspicious > 0:
        return {"message": "URL is not safe"}

    return {"message": "URL is safe"}
