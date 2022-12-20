import asyncio
from datetime import datetime, timedelta

from models import *
from db_access.globals import *


# Windows specific issue https://stackoverflow.com/questions/61543406/asyncio-run-runtimeerror-event-loop-is-closed
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# file_path = r"./_init_db/init_db.txt"
file_path = r"server/_init_db/messages.txt"
def get_messages(alice:str, bob:str) -> list[Message]:
    """" Load pre made messages """
    read = []
    try:
        with open(file_path) as f:
            read = f.readlines()
    except FileNotFoundError as e:
        print(f"lmao\n{e}\nignore this")

    messages = []
    back_to_the_future = len(read) * 18
    for i, x in enumerate(read):
        room, user, content = x.split(",")
        user_id = bob if user == "bob" else alice
        content = content[1:-2]
        msg = Message(user_id, room, content)
        msg.time = datetime.now() + timedelta(seconds=17*i - back_to_the_future)
        messages.append(msg)

    return messages



async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        async with session.begin():
            bob = User("bob", "bob@gmail.com", "bob123")
            alice = User("alice", "alice@yahoo.com", "alice456")
            bob.avatar = "/galaxy.jpg"
            alice.avatar = "/default.png"
            session.add(bob)
            session.add(alice)

        async with session.begin():
            for msg in get_messages(alice.user_id, bob.user_id):
                session.add(msg)


asyncio.run(main())
