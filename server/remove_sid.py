import asyncio
import sqlalchemy as sa
from db_access.globals import async_session
from models import SioConnection


async def main():
    statement = sa.delete(SioConnection)
    async with async_session() as session:
        async with session.begin():
            await session.execute(statement)

    print("All SIDs delete LMAO.")


asyncio.run(main())
