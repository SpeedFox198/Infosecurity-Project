from quart import Blueprint, request, json
from quart_auth import (
    login_required,
    current_user
)


group_bp = Blueprint("group", __name__, url_prefix="/group")


@group_bp.post("/new")
@login_required
async def create_group():
    group_photo = (await request.files).get("group_photo")
    metadata = json.loads(
        (await request.form).get("metadata")
    )
    print(group_photo, metadata)

    # TODO Implement DB logic
    """-- Code Here --"""
    return {"message": "ball"}, 200
