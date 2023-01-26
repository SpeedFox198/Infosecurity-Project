import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError

import models
from db_access.globals import async_session
from models import BackupCodes
from blueprints.auth.functions import generate_otp
from utils.logging import log_exception

#Create 2FA backup codes
async def create_2fa_backup_codes(user_id) -> None:
    async with async_session() as session:
        for _ in range(6):
            code = await generate_otp()
            statement = sa.insert(models.BackupCodes).values(user_id=user_id, code=code)
            try:
                await session.execute(statement)
                await session.commit()
            except SQLAlchemyError as err:
                await log_exception(err)

#Retrieve 2FA backup codes
async def get_2fa_backup_codes(user_id) -> list[BackupCodes] | None:
    async with async_session() as session:
        statement = sa.select(models.BackupCodes).where(models.BackupCodes.user_id == user_id)
        result = await session.execute(statement)
        backup_codes = result.scalars().all()
        if backup_codes:
            return backup_codes
        else:
            return None

#Delete one specific 2FA backup code
async def delete_2fa_backup_codes(user_id, code):
    async with async_session() as session:
        statement = sa.delete(models.BackupCodes).where(models.BackupCodes.user_id == user_id).where(models.BackupCodes.code == code)
        try:
            await session.execute(statement)
            await session.commit()
        except SQLAlchemyError as err:
            await session.rollback()
            await log_exception(err)

async def delete_2fa_backup_codes_all(user_id):
    async with async_session() as session:
        statement = sa.delete(models.BackupCodes).where(models.BackupCodes.user_id == user_id)
        try:
            await session.execute(statement)
            await session.commit()
        except SQLAlchemyError as err:
            await session.rollback()
            await log_exception(err)