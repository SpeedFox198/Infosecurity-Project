from datetime import datetime, timedelta

from db_access.globals import Base
from models import Message
from sqlalchemy import CHAR, TIMESTAMP, Column, ForeignKey


class Disappearing(Base):
    __tablename__ = "disappearing"

    def __init__(self, message_id:str, **kwargs:int) -> None:
        """
        Creates a record for disappearing messages

        *MAGIC! POOF! DISAPPEAR!*  ^ ̳ට ̫ ට ̳^

        (๑°༥°๑) (๑°༥°๑) (๑°༥°๑) (๑°༥°๑) (๑°༥°๑)

        Args:
            message_id(str): message_id of the message to be deleted
            seconds(int): Number of seconds the message remains before it disappears
            days(int): Number of days the message remains before it disappears
            weeks(int): Number of weeks the message remains before it disappears
        """
        self.message_id = message_id
        self.time = datetime.now() + timedelta(**kwargs)

    message_id = Column(CHAR(36), ForeignKey(Message.message_id), primary_key=True)
    time = Column(TIMESTAMP())
