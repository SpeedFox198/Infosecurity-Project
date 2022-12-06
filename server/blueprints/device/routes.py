import time

from quart import Blueprint
import sqlalchemy as sa
from quart_auth import (
    login_required,
    current_user
)

from db_access.globals import async_session
from models import (
    Device
)

device_bp = Blueprint("device", __name__, url_prefix="/device")


@device_bp.get("/")
@login_required
async def get_devices():
    async with async_session() as session:
        statement = sa.select(Device).where(Device.user_id == await current_user.user_id)
        results = await session.execute(statement)
        device_list = results.scalars()

    # the results are unsorted because of async (maybe)
    unsorted_device_list = [
        {
            "id": device.device_id,
            "time": int(time.mktime(device.time.timetuple())),  # unix time
            "location": device.location,
            "os": device.os,
            "browser": device.browser
        }
        for device in device_list
    ]
    # sort by time
    return sorted(unsorted_device_list, key=lambda i: i["time"], reverse=True)
