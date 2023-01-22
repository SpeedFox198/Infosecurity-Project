import asyncio
from datetime import datetime, timedelta

from db_access.globals import *
from models import *
from security_functions.cryptography import pw_hash

ROOM_GROUP_NUM = 4  # Number of groups group chats
ROOM_DIRECT_NUM = 2  # Number of direct group chats

# PATH_MESSAGES = r"./_init_db/messages.txt"
# PATH_GROUPS = r"./_init_db/groups.txt"
# PATH_MEMBERSHIPS = r"./_init_db/memberships.txt"
PATH_MESSAGES = r"server/_init_db/messages.txt"
PATH_GROUPS = r"server/_init_db/groups.txt"
PATH_MEMBERSHIPS = r"server/_init_db/memberships.txt"


# Windows specific issue https://stackoverflow.com/questions/61543406/asyncio-run-runtimeerror-event-loop-is-closed
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def read_from_file(file_path):
    read = []
    try:
        with open(file_path) as f:
            read = f.readlines()
    except FileNotFoundError as e:
        print(f"lmao\n{e}\nignore this")
    return [i[:-1] for i in read]


async def add_rooms(session):
    rooms = [Room("off", type_="group") for _ in range(ROOM_GROUP_NUM)]
    rooms.extend([Room("off") for _ in range(ROOM_DIRECT_NUM)])
    rooms[-1].encrypted = True
    async with session.begin():
        for room in rooms:
            session.add(room)
    # Cuz room this room is bob and carol dm, it's e2ee (i set it that way)
    return rooms


async def add_groups(session, room_ids):
    read = read_from_file(PATH_GROUPS)
    groups = []
    for data, room_id in zip(read, room_ids[:ROOM_GROUP_NUM]):
        args = [i for i in data.split(",") if i]
        groups.append(Group(room_id, *args))

    async with session.begin():
        for grp in groups:
            session.add(grp)


async def add_friends(session, alice, bob, carol):
    async with session.begin():
        session.add(Friend(alice, bob))
        session.add(Friend(bob, carol))


async def add_memberships(session, room_ids, alice, bob, carol):
    read = read_from_file(PATH_MEMBERSHIPS)
    mnm = []  # forgive me for the name im dyin
    for data in read:
        room, user, admin = data.split(",")
        room_id = room_ids[int(room) - 1]
        user_id = {"alice": alice, "bob": bob, "carol": carol}[user]
        is_admin = admin == "True"
        mnm.append(Membership(room_id, user_id, is_admin))

    async with session.begin():
        for m in mnm:
            session.add(m)


async def add_users(session):
    async with session.begin():
        alice = User("alice", "alice@yahoo.com", pw_hash("alice456"))
        bob = User("bob", "bob@gmail.com", pw_hash("bob123"))
        carol = User("carol", "carol@outlook.com", pw_hash("carol789"))
        alice.avatar = "/default.png"
        bob.avatar = "/galaxy.jpg"
        carol.avatar = "/murder.jpg"
        # for now use same key LMAO cuz i lazy (if got time, prob not, change this)
        bob.public_key = "BNBP/IX/gJRrfQTWE3eDJJ6BmDSsjspXt7SuWkmG4DAUVhN6JrVxKC2DY16JqDxglw4Wf6D1tdTBL6hQp81HlbE="
        carol.public_key = "BNBP/IX/gJRrfQTWE3eDJJ6BmDSsjspXt7SuWkmG4DAUVhN6JrVxKC2DY16JqDxglw4Wf6D1tdTBL6hQp81HlbE="
        session.add(bob)
        session.add(alice)
        session.add(carol)

    return alice, bob, carol


async def get_messages(session, room_ids, alice, bob, carol):
    """" Load pre made messages """
    read = read_from_file(PATH_MESSAGES)

    messages = []
    back_to_the_future = len(read) * 18
    for i, x in enumerate(read):
        room, user, content = x.split(",")
        user_id = {"alice": alice, "bob": bob, "carol": carol}[user]
        room_id = room_ids[int(room) - 1]
        msg = Message(user_id, room_id, content)
        msg.time = datetime.now() + timedelta(seconds=17 * i - back_to_the_future)
        messages.append(msg)

    async with session.begin():
        for msg in messages:
            session.add(msg)


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        rooms = await add_rooms(session)
        room_ids = [i.room_id for i in rooms]
        await add_groups(session, room_ids)
        alice, bob, carol = await add_users(session)
        await add_friends(session, alice.user_id, bob.user_id, carol.user_id)
        await add_memberships(session, room_ids, alice.user_id, bob.user_id, carol.user_id)
        await get_messages(session, room_ids, alice.user_id, bob.user_id, carol.user_id)


asyncio.run(main())
