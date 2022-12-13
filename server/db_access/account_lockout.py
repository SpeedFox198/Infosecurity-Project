from datetime import datetime
import sqlalchemy as sa
from db_access.globals import async_session
from models import Lockout

#Create lockout
async def create_lockout(user_id):
    async with async_session() as session:
        statement = sa.insert(Lockout).values(user_id=user_id, lockout=datetime.now())
        try:
            await session.execute(statement)
            await session.commit()
        except:
            return False

#Retrieve lockout
async def get_lockout(user_id):
    async with async_session() as session:
        statement = sa.select(Lockout).where(Lockout.user_id == user_id)
        result = await session.execute(statement)
        lockout = result.scalars().first()
        if lockout:
            return lockout
        return False

#Delete lockout
async def delete_lockout(user_id):
    async with async_session() as session:
        statement = sa.delete(Lockout).where(Lockout.user_id == user_id)
        try:
            await session.execute(statement)
            await session.commit()
        except:
            return False