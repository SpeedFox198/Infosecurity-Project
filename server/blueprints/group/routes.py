from quart import Blueprint, request, json
from quart.datastructures import FileStorage
from quart_auth import (
    login_required,
    current_user
)


group_bp = Blueprint("group", __name__, url_prefix="/group")


@group_bp.post("/new")
@login_required
async def create_group():
    group_photo: FileStorage | None = (await request.files).get("group_photo")
    metadata: dict = json.loads(
        (await request.form).get("metadata")
    )

    # TODO Implement DB logic
    """-- Code Here --"""
    return {"message": "ball"}, 200
