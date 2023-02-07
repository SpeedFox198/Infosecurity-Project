import sqlalchemy as sa
import os
from db_access.globals import async_session
from models import Membership, Media, Message
from quart import Blueprint, abort, current_app, send_from_directory, send_file
from quart_auth import current_user, login_required
from werkzeug.utils import secure_filename
from sqlalchemy.orm.exc import NoResultFound

media_bp = Blueprint("media", __name__, url_prefix="/media")


@media_bp.route("/attachments/<string:room_id>/<string:message_id>/<string:filename>", methods=["GET", "POST"])
@login_required
async def attachments(room_id: str, message_id: str, filename: str):
    current_user_id = await current_user.user_id

    async with async_session() as session:

        # Check if user is member of room
        statement = sa.select(Membership).where(
            (Membership.user_id == current_user_id) &
            (Membership.room_id == room_id)
        )

        try:
            (await session.execute(statement)).one()
        except NoResultFound:
            abort(404)  # If not a member of room, do not let user know file exist

        statement = sa.select(Media.path).where(Media.message_id == message_id)

        try:
            result = (await session.execute(statement)).one()
        except NoResultFound:
            abort(404)  # If message_id invalid, do not let user know file exist

        if filename != result[0]:
            abort(404)  # If not a filename not in results, do not let user know file exist

        file_type_statement = sa.select(Message.type).where(Message.message_id == message_id)
        file_type = (await session.execute(file_type_statement)).scalar()

    directory = os.path.join(current_app.config["ATTACHMENTS_PATH"], room_id, message_id)

    if file_type in ("document", "text"):
        # Download file when they visit the url
        directory = os.path.join(directory, secure_filename(filename))
        return await send_file(directory, as_attachment=True)

    # Secure filename just in case
    return await send_from_directory(directory, secure_filename(filename))


# TODO(medium)(SpeedFox198): validate_request, and also verify user is logged in
@media_bp.get("/filename/<string:message_id>")
@login_required
async def get_filename(message_id: str):

    async with async_session() as session:
        statement = sa.select(Media.path, Media.height, Media.width).where(Media.message_id == message_id)

        try:
            result = (await session.execute(statement)).one()
        except NoResultFound:
            abort(404)

    return {
        "filename": secure_filename(result[0]),
        "height": result[1],
        "width": result[2]
    }


# TODO Add route for showing group icons
@media_bp.get("/icon/<string:group_id>/<string:filename>")
@login_required
async def get_group_icon(group_id: str, filename: str):
    return await send_from_directory(os.path.join("media/icon", group_id), filename)
