from pydantic import ValidationError
from quart import Blueprint, request, json
from quart.datastructures import FileStorage
from quart_auth import (
    login_required,
    current_user
)

from blueprints.group.functions import save_group_icon
from db_access.globals import async_session
from models import Room, Group, Membership
from models.request_data import GroupMetaDataBody

group_bp = Blueprint("group", __name__, url_prefix="/group")


@group_bp.post("/new")
@login_required
async def create_group():
    # TODO Add validation
    group_icon: FileStorage | None = (await request.files).get("group_icon")
    
    try:
        group_metadata = GroupMetaDataBody(
            **json.loads(
                (await request.form).get("metadata")
            )
        )
    except ValidationError as err:
        error_list = [error["msg"] for error in err.errors()]
        error_message = ", ".join(error_list)
        return {"message": error_message}, 400

    async with async_session() as session:
        # Create new room
        new_room = Room(group_metadata.disappearing, "group")
        session.add(new_room)
        await session.flush()

        if group_icon:
            # Add Group icon if any and the group details
            icon_path = await save_group_icon(new_room, group_icon)

            session.add(
                Group(new_room.room_id, group_metadata.name, icon_path)
            )
            await session.flush()
        else:
            session.add(
                Group(new_room.room_id, group_metadata.name)
            )
            await session.flush()

        # Add the current user as admin of the group
        session.add(
            Membership(new_room.room_id, await current_user.user_id, is_admin=True)
        )
        await session.flush()

        # Add the included users to the group
        for user_id in group_metadata.users:
            session.add(
                Membership(new_room.room_id, user_id)
            )
            await session.flush()

        await session.commit()

    return {"message": "Group added successfully!"}, 200
