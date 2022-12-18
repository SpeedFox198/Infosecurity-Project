from datetime import datetime

import sqlalchemy as sa
from db_access.globals import async_session
from models import Disappearing

from .peek_queue import PeekQueue

# TODO(SpeedFox198):
# For now, only implement disappearing messages in 15 seconds
# Make it check every 3 seconds
# And also for now load all message from db without care for the freaking universe
# LMAO
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


    async def init_from_db(self) -> None:
        """ Initialise queue by fetching from database """
        self.__init__(await self.get_disappearing_messages())


    @staticmethod
    async def get_disappearing_messages() -> list[Disappearing]:
        """ Retrieves and returns records of disappearing messages from database """
        async with async_session() as session:
            # TODO(SpeedFox198): need to add limit
            statement = sa.select(Disappearing).order_by(Disappearing.time)
            result = (await session.execute(statement)).all()

        return [row[0] for row in result]


    def delete_expired(self) -> list[str]:

        deleted = []  # Stores messages_id of deleted messages

        while self.has_expired_messages:
            deleted.append(self.get().message_id)

        return deleted


    # TODO(SpeedFox198): Add time paramater?
    async def add_disappearing_messages(self, message_id:str, **kwargs):

        # Create new record of message to disappear
        record = Disappearing(message_id, **kwargs)

        async with async_session() as session:
            async with session.begin():
                session.add(record)

        self.put(record)


    async def delete_disappearing_messages(self):
        # Delete records from queue
        expired = self.delete_expired()

        # Delete records from database
        async with async_session() as session:

            statement = sa.delete(Disappearing).where(Disappearing.message_id.in_(expired))
            await session.execute(statement)
            await session.commit()

        return expired


    async def check_disappearing_messages(self, callback):
        if self.has_expired_messages:
            expired = await self.delete_disappearing_messages()
            await callback(expired)
