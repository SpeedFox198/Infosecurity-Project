import asyncio
import sqlalchemy as sa
from db_access.globals import async_session
from models import Disappearing
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .peek_queue import PeekQueue

# TODO(SpeedFox198):
# For now, only implement disappearing messages in 15 seconds
# Make it check every 3 seconds
# And also for now load all message from db without care for the freaking universe
# http://mysql.rjweb.org/doc.php/deletebig
# https://dev.mysql.com/doc/refman/5.7/en/partitioning.html


class DisappearingQueue(PeekQueue):
    """
    Stores a queue of records of disappearing messages
    """

    @property
    def has_expired_messages(self) -> bool:
        if self.empty():
            return False
        oldest_record = self.peek()
        now = datetime.now()
        return oldest_record.time <= now


    def delete_expired(self) -> list[str]:

        deleted = []  # Stores messages_id of deleted messages

        while self.has_expired_messages:
            deleted.append(self.get().message_id)

        return deleted


async def get_disappearing_messages():
    async with async_session() as session:
        # TODO(SpeedFox198): need to add limit
        statement = sa.select(Disappearing).order_by(Disappearing.time)
        result = (await session.execute(statement)).all()

    return DisappearingQueue([row[0] for row in result])


# TODO(SpeedFox198): Add time paramater?
async def add_disappearing_messages(message_id:str, **kwargs):

    # Create new record of message to disappear
    record = Disappearing(message_id, **kwargs)

    async with async_session() as session:
        async with session.begin():
            session.add(record)

    messages_queue.put(record)


async def delete_disappearing_messages():
    # Delete records from queue
    expired = messages_queue.delete_expired()

    # Delete records from database
    async with async_session() as session:

        statement = sa.delete(Disappearing).where(Disappearing.message_id.in_(expired))
        await session.execute(statement)
        await session.commit()

    return expired


async def check_disappearing_messages(callback):
    if messages_queue.has_expired_messages:
        expired = await delete_disappearing_messages()
        await callback(expired)


messages_queue = asyncio.run(get_disappearing_messages())
