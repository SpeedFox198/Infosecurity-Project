import sqlalchemy as sa
from db_access.globals import async_session
from models import Disappearing, Media, Membership, Message, Room
from utils import to_unix


async def db_get_room_messages(room_id: str, limit: int, offset: int) -> list[dict]:
    """ Get room messages from database """
    async with async_session() as session:
        statement = sa.select(
            Message.message_id,
            Message.user_id,
            Message.time,
            Message.content,
            Message.type,
            Message.encrypted
        ).where(
            Message.room_id == room_id
        ).order_by(Message.time.desc()).limit(limit).offset(offset)

        result: list[Message] = (await session.execute(statement)).all()

    # Create list of messages represented in JSON in reverse order
    room_messages = [{
        "message_id": result[i].message_id,
        "user_id": result[i].user_id,
        "time": to_unix(result[i].time),
        "content": result[i].content,
        "type": result[i].type,
        "encrypted": result[i].encrypted
    } for i in range(len(result) - 1, -1, -1)]

    return room_messages


async def db_remove_messages(messages: list[str], room_id: str, user_id: str) -> list[str]:
    """ Delete messages from database (ensures that room_id is correct) """
    async with async_session() as session:

        # Get room type details
        statement = sa.select(Room.type).where(Room.room_id == room_id)
        room_type = (await session.execute(statement)).one()[0]

        if room_type == "direct":  # User's can't delete other's messages in direct chats
            is_admin = False
        else:
            # Check if user is group admin
            statement = sa.select(Membership.is_admin).where(
                (Membership.user_id == user_id) &
                (Membership.room_id == room_id)
            )
            is_admin = (await session.execute(statement)).one()[0]

        condition = (Message.message_id.in_(messages)) & (Message.room_id == room_id)

        # If user is not admin of group chat, only allow deletion of own messages
        if not is_admin:
            condition &= (Message.user_id == user_id)

        # Get messages to delete
        statement = sa.select(Message.message_id).where(condition)

        result = (await session.execute(statement)).all()
        messages = [row[0] for row in result]

        # Delete messages from database
        statement = sa.delete(Media).where(Media.message_id.in_(messages))
        await session.execute(statement)

        statement = sa.delete(Disappearing).where(Disappearing.message_id.in_(messages))
        await session.execute(statement)

        statement = sa.delete(Message).where(Message.message_id.in_(messages))
        await session.execute(statement)

        await session.commit()

    return messages


async def db_get_room_id_of_message(message_id: str):
    async with async_session() as session:
        statement = sa.select(Message.room_id).where(Message.message_id == message_id)
        return (await session.execute(statement)).scalar()
