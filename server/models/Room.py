from sqlalchemy import (
    Column,
    CHAR,
    Boolean,
)
from sqlalchemy.dialects.mysql import ENUM

from db_access.globals import Base


class Room(Base):
    __tablename__ = "Room"

    room_id = Column(CHAR(36), primary_key=True)
    disappearing = Column(Boolean, default=False)
    type = Column(ENUM("direct", "group"))
