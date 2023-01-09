import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError

from db_access.globals import async_session
from models import BackupCodes
from blueprints.auth.functions import generate_otp
from utils.logging import log_exception

#Create 2FA backup codes
async def create_2fa_backup_codes(user_id) -> None:
    async with async_session() as session:
        code1 = generate_otp()
        code2 = generate_otp()
        code3 = generate_otp()
        code4 = generate_otp()
        code5 = generate_otp()
        code6 = generate_otp()
        statement = sa.insert(BackupCodes).values(user_id=user_id, code1=code1, code2=code2, code3=code3, code4=code4, code5=code5, code6=code6)
        try:
            await session.execute(statement)
            await session.commit()
        except SQLAlchemyError as err:
            await log_exception(err)

#Retrieve 2FA backup codes
async def get_2fa_backup_codes(user_id) -> BackupCodes | None:
    async with async_session() as session:
        statement = sa.select(BackupCodes).where(BackupCodes.user_id == user_id)
        result = await session.execute(statement)
        backup_codes = result.scalars().first()
        if backup_codes:
            return backup_codes
        else:
            return None

#Delete 2FA backup codes
async def delete_2fa_backup_codes(user_id):
    async with async_session() as session:
        statement = sa.delete(BackupCodes).where(BackupCodes.user_id == user_id)
        try:
            await session.execute(statement)
            await session.commit()
        except SQLAlchemyError as err:
            await session.rollback()
            await log_exception(err)