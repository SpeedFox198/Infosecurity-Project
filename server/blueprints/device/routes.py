from quart import Blueprint
import sqlalchemy as sa
from quart_auth import (
    login_required,
    current_user
)
from quart_schema import validate_response

from db_access.device import remove_logged_in_device
from db_access.globals import async_session
from models import Device
from models.response_data import DeviceListData, DeviceData
from utils import to_unix
from utils.logging import log_info

device_bp = Blueprint("devices", __name__, url_prefix="/devices")


@device_bp.get("/")
@login_required
@validate_response(DeviceListData)
async def get_devices():
    async with async_session() as session:
        statement = sa.select(Device)\
            .where(Device.user_id == await current_user.user_id)\
            .order_by(sa.desc(Device.time))
        results = await session.execute(statement)
        device_results = results.scalars()

    device_list = DeviceListData([
        DeviceData(
            device.device_id,
            to_unix(device.time),
            device.location,
            device.os,
            device.browser
        )
        for device in device_results
    ])

    return device_list


@device_bp.delete("/<string:device_id>")
@login_required
async def remove_device(device_id):
    status = await remove_logged_in_device(device_id, await current_user.user_id)
    if status == "fail":
        return {"message": "failed to remove device"}, 404

    await log_info(f"{current_user.username} has removed device {device_id}")
    return {"message": "device removed successfully"}
