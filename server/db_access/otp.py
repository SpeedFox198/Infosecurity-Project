import sqlalchemy as sa
from db_access.globals import async_session
from models import User

#Create OTP
async def create_otp(user_id, otp, password):
    async with async_session() as session:
        statement = sa.insert(User).values(user_id=user_id, otp=otp, password=password)
        try:
            await session.execute(statement)
            await session.commit()
        except:
            return False

#Retrieve OTP
async def get_otp(user_id):
    async with async_session() as session:
        statement = sa.select(User).where(User.user_id == user_id)
        result = await session.execute(statement)
        otp = result.scalars().first()
        if otp:
            return otp
        return False

#Delete OTP
async def delete_otp(user_id):
    async with async_session() as session:
        statement = sa.delete(User).where(User.user_id == user_id)
        try:
            await session.execute(statement)
            await session.commit()
        except:
            return False