# Maybe we want to store cookies in the server so that we can validate with logged-in sessions
# Will need device_id and user_id
# the validation may be done before a request or something
# request.cookies.get("QUART_AUTH") - Get the cookie string
from sqlalchemy.exc import SQLAlchemyError

from db_access.globals import async_session
import sqlalchemy as sa
from models import Device


async def get_device(user_id: str, device_id: str):
    async with async_session() as session:
        statement = sa.select(Device).where(
            (Device.user_id == user_id)
            &
            (Device.device_id == device_id)
        )

        try:
            result = await session.execute(statement)
            return result.scalars().first()
        except SQLAlchemyError as err:
            await session.rollback()
            print(err)

