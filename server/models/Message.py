from datetime import datetime
from uuid import uuid4

from db_access.globals import Base
from models import Room, User
from sqlalchemy import CHAR, TIMESTAMP, VARCHAR, Column, ForeignKey
from sqlalchemy.dialects.mysql import ENUM


class Message(Base):
    __tablename__ = "message"

    def __init__(self, user_id: str, room_id: str, content: str, reply_to: str = None, type_: str = "text"):
        self.message_id = str(uuid4())
        self.user_id = user_id
        self.room_id = room_id
        self.time = datetime.now()
        self.content = content
        self.reply_to = reply_to
        self.type = type_

    message_id = Column(CHAR(36), primary_key=True)
    user_id = Column(CHAR(36), ForeignKey(User.user_id))
    room_id = Column(CHAR(36), ForeignKey(Room.room_id))
    time = Column(TIMESTAMP())
    content = Column(VARCHAR(2000))
    reply_to = Column(CHAR(36))
    type = Column(ENUM("image", "document", "video", "text"))
