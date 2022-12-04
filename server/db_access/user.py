import sqlalchemy as sa

from db_access.globals import async_session
from models.User import User


async def get_user_details(user_id: str) -> tuple:
    async with async_session() as session:
        statement = sa.select(
                User.username,
                User.email,
                User.profile_pic,
                User.dark_mode,
                User.malware_scan,
                User.friends_only,
                User.censor
        ).where(User.user_id == user_id)
        result = await session.execute(statement)
        return result.first()
