from sqlalchemy import (
    Column,
    CHAR,
    TIMESTAMP,
    VARCHAR,
    ForeignKey,
)
from sqlalchemy.dialects.mysql import ENUM

from server.db_access.globals import Base
from server.models import User, Room


class Message(Base):
    __tablename__ = "Message"

    message_id = Column(CHAR(36), primary_key=True)
    user_id = Column(CHAR(36), ForeignKey(User.user_id))
    room_id = Column(CHAR(36), ForeignKey(Room.room_id))
    time = Column(TIMESTAMP())
    content = Column(VARCHAR(2000))
    reply_to = Column(CHAR(36))
    type = Column(ENUM("image", "document", "video", "text"))
