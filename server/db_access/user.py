import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError

from db_access.globals import async_session
from models.User import User


async def get_user_details(user_id: str) -> tuple:
    async with async_session() as session:
        statement = sa.select(
                User.username,
                User.email,
                User.avatar,
                User.public_key,
                User.dark_mode,
                User.malware_scan,
                User.friends_only,
                User.censor,
                User.twofa_status
        ).where(User.user_id == user_id)
        result = await session.execute(statement)
        return result.first()


async def insert_user_by_google(user_id: str, username: str, email: str, avatar: str) -> None:
    async with async_session() as session:
        statement = sa.insert(User).values(user_id=user_id, username=username, email=email, avatar=avatar)
        try:
            await session.execute(statement)
            await session.commit()
            print("success")
        except SQLAlchemyError as err:
            await session.rollback()
            raise err