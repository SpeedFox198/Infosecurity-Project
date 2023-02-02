from sqlalchemy import (
    Column,
    CHAR,
    ForeignKey,
    Boolean
)
from sqlalchemy.orm import relationship

from db_access.globals import Base
from models import Message, Room


class MessageStatus(Base):
    __tablename__ = "message_status"

    def __init__(self, message_id, room_id):
        self.message_id = message_id
        self.room_id = room_id

    message_id = Column(CHAR(36), ForeignKey(Message.message_id), primary_key=True)
    room_id = Column(CHAR(36), ForeignKey(Room.room_id))
    read_by_recipient = Column(Boolean, default=False)
    malicious = Column(Boolean, default=False)
    
    message = relationship("Message", back_populates="status", uselist=False, lazy="joined")
