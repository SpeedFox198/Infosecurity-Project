import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError

from db_access.globals import async_session
from models.User import User
from utils.logging import log_exception


async def get_user_details(user_id: str) -> tuple | None:
    async with async_session() as session:
        statement = sa.select(
                User.username,
                User.email,
                User.avatar,
                User.e2ee,
                User.public_key,
                User.dark_mode,
                User.malware_scan,
                User.friends_only,
                User.censor,
                User.google_account,
                User.disappearing
        ).where(User.user_id == user_id)
        result = await session.execute(statement)
        return result.first()


async def insert_user_by_google(user_id: str, username: str, email: str, avatar: str) -> None:
    async with async_session() as session:
        statement = sa.insert(User).values(user_id=user_id, username=username, email=email, avatar=avatar, e2ee=True)
        try:
            await session.execute(statement)
            await session.commit()
        except SQLAlchemyError as err:
            await session.rollback()
            await log_exception(err)
            raise err


# Reset password with email and replace with new password
async def reset_password_with_email(email: str, password: str) -> None:
    async with async_session() as session:
        statement = sa.update(User).where(User.email == email).values(password=password)
        try:
            await session.execute(statement)
            await session.commit()
        except SQLAlchemyError as err:
            await session.rollback()
            await log_exception(err)
            raise err


# Get user_id from email
async def get_user_id(email: str) -> str | None:
    async with async_session() as session:
        statement = sa.select(User.user_id).where(User.email == email)
        result = await session.execute(statement)
        return result.scalar()


async def db_set_user_public_key(user_id: str, public_key: str):
    async with async_session() as session:
        statement = sa.update(User).where(User.user_id == user_id).values(public_key=public_key)
        try:
            await session.execute(statement)
            await session.commit()
        except SQLAlchemyError as err:
            await log_exception(err)


async def db_set_user_wrap_key(user_id: str, wrap_key: str):
    async with async_session() as session:
        statement = sa.update(User).where(User.user_id == user_id).values(wrap_key=wrap_key)
        try:
            await session.execute(statement)
            await session.commit()
        except SQLAlchemyError as err:
            await log_exception(err)


async def db_reset_all_users_online_status():
    """ Resets all users' online status to offline """
    try:
        statement = sa.update(User).where(User.online == True).values(online = False)
        async with async_session() as session:
            async with session.begin():
                await session.execute(statement)
    except SQLAlchemyError as err:
        await log_exception(err)


async def db_enable_user_e2ee(user_id: str):
    async with async_session() as session:
        statement = sa.update(User).where(User.user_id == user_id).values(e2ee=True)
        try:
            await session.execute(statement)
            await session.commit()
        except SQLAlchemyError as err:
            await log_exception(err)
