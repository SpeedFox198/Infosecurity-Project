from uuid import uuid4

from db_access.globals import Base
from sqlalchemy import CHAR, Column, VARCHAR
from sqlalchemy.dialects.mysql import ENUM


class Room(Base):  # TODO(high)(SpeedFox198): change disappearing to 3 options (change docs too)
    # TODO Change the checking of disappearing logic in sio.py
    __tablename__ = "room"

    def __init__(self, disappearing: str, type_: str = "direct"):
        """
        Creates a room object

        Args:
            disappearing(str): Off (off) / 24 Hours (24h) /7 Days (7d) /30 Days (30d)
            type_(:obj:`str`, optional): Type of chat room ("direct" or "group")

        Raises:
            ValueError: If `type_` is neither "direct" nor "group"
        """
        if type_ not in ("direct", "group"):
            raise ValueError('type_ must be either "direct" or "group"')

        self.room_id = str(uuid4())
        self.disappearing = disappearing
        self.type = type_

    room_id = Column(CHAR(36), primary_key=True)
    disappearing = Column(ENUM("off", "24h", "7d", "30d"))
    type = Column(ENUM("direct", "group"))
