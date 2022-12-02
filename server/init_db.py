import asyncio

from sqlalchemy import select
from server.models import User, Room
from server.db_access.globals import *


# Windows specific issue https://stackoverflow.com/questions/61543406/asyncio-run-runtimeerror-event-loop-is-closed
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        async with session.begin():
            session.add(User("bob", "bob@gmail.com", "bob123"))
            session.add(User("alice", "alice@yahoo.com", "alice456"))


async def query():
    async with async_session() as session:
        stmt = select(User)
        result = await session.execute(stmt)
        for item in result.scalars():
            print(item.username)


asyncio.run(main())
