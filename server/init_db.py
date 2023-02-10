import asyncio
import os
from datetime import datetime, timedelta

from db_access.globals import *
from models import *
from security_functions.cryptography import pw_hash

ROOM_GROUP_NUM = 4  # Number of groups group chats
ROOM_DIRECT_NUM = 2  # Number of direct group chats

if os.getcwd().split("\\")[-1] == "server":
    PATH_MESSAGES = r"./_init_db/messages.txt"
    PATH_GROUPS = r"./_init_db/groups.txt"
    PATH_MEMBERSHIPS = r"./_init_db/memberships.txt"
else:
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

    # hardcode alice-bob direct message
    rooms[4].room_id = "95389c76-ad62-41c4-9993-006f1b9a1bc4"

    async with session.begin():
        for room in rooms:
            session.add(room)
    # Cuz room this room is bob and clarence dm, it's e2ee (i set it that way)
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


async def add_friends(session, alice, bob, clarence):
    async with session.begin():
        session.add(Friend(alice, bob))
        session.add(Friend(bob, clarence))


async def add_memberships(session, room_ids, alice, bob, clarence):
    read = read_from_file(PATH_MEMBERSHIPS)
    mnm = []  # forgive me for the name im dying
    for data in read:
        room, user, admin = data.split(",")
        room_id = room_ids[int(room) - 1]
        user_id = {"alice": alice, "bob": bob, "clarence": clarence}[user]
        is_admin = admin == "True"
        mnm.append(Membership(room_id, user_id, is_admin))

    async with session.begin():
        for m in mnm:
            session.add(m)


async def add_users(session):
    async with session.begin():
        alice = User("alice", "alice@yahoo.com", pw_hash("alice456"))
        bob = User("bob", "bob@gmail.com", pw_hash("bob123"))
        clarence = User("clarence", "clarence@outlook.com", pw_hash("cats!"))
        daniel = User("daniel", "daniel@dynamicprogramming.com", pw_hash("daniel123"))
        eden = User("eden", "eden@joker.com", pw_hash("eden789"))

        alice.avatar = "/default.png"
        bob.avatar = "/galaxy.jpg"
        clarence.avatar = "/murder.jpg"
        daniel.avatar = "/COVID SPREADS DIGITALLY.png"
        eden.avatar = "/ALL THE BEST EMOJI.png"

        # for now use same key LMAO cuz i lazy (if got time, prob not, change this)
        bob.public_key = "BNCmIGKDCCY70oo6r+6rx7eyrPrl+E0VA6WbMHSs4ZmauaC+vDjSHVN3y3k1euAvzDhNWKYLBQ/S01odkKFqpOo="
        clarence.public_key = "BNCmIGKDCCY70oo6r+6rx7eyrPrl+E0VA6WbMHSs4ZmauaC+vDjSHVN3y3k1euAvzDhNWKYLBQ/S01odkKFqpOo="
        bob.e2ee = True
        clarence.e2ee = True

        alice.user_id = "7773099b-666c-4dd2-b494-ea51715afe97"
        bob.user_id = "2eba00ba-5d53-4fb9-b316-3f346bd830e7"

        session.add(bob)
        session.add(alice)
        session.add(clarence)
        session.add(daniel)
        session.add(eden)

    return alice, bob, clarence


async def add_messages(session, room_ids, alice, bob, clarence):
    """" Load pre made messages """
    read = read_from_file(PATH_MESSAGES)

    messages = []
    back_to_the_future = len(read) * 18
    for i, x in enumerate(read):
        room, user, content = x.split(",")
        user_id = {"alice": alice, "bob": bob, "clarence": clarence}[user]
        room_id = room_ids[int(room) - 1]
        msg = Message(user_id, room_id, content)
        msg_status = MessageStatus(msg.message_id, room_id)
        msg.time = datetime.now() + timedelta(seconds=17 * i - back_to_the_future)
        msg.status = msg_status
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
        alice, bob, clarence = await add_users(session)
        await add_friends(session, alice.user_id, bob.user_id, clarence.user_id)
        await add_memberships(session, room_ids, alice.user_id, bob.user_id, clarence.user_id)
        await add_messages(session, room_ids, alice.user_id, bob.user_id, clarence.user_id)

    print("Database initialised! :)")


asyncio.run(main())
