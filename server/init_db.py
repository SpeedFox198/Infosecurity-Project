import asyncio

from sqlalchemy import select
from models import *
from db_access.globals import *


# Windows specific issue https://stackoverflow.com/questions/61543406/asyncio-run-runtimeerror-event-loop-is-closed
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        async with session.begin():
            # bob = User("bob", "bob@gmail.com", "bob123")
            # alice = User("alice", "alice@yahoo.com", "alice456")
            # bob.user_id = "2a3f14df-ef17-4410-baf9-ed6693ac8c5a"
            # alice.user_id = "ac4528d0-98f3-41a3-9516-03381f76c374"
            # session.add(bob)
            # session.add(alice)
            session.add(User("bob", "bob@gmail.com", "bob123"))
            session.add(User("alice", "alice@yahoo.com", "alice456"))


async def query():
    async with async_session() as session:
        stmt = select(User)
        result = await session.execute(stmt)
        for item in result.scalars():
            print(item.username)


asyncio.run(main())
