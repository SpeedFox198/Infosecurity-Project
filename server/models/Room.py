from sqlalchemy import (
    Column,
    CHAR,
    Boolean,
    VARCHAR
)

from db_access.globals import Base


class Room(Base):
    __tablename__ = "Room"

    room_id = Column(CHAR(36), primary_key=True)
    room_pic = Column(VARCHAR(255))
    disappearing = Column(Boolean)
