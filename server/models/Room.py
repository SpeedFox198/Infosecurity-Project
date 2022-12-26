from uuid import uuid4

from db_access.globals import Base
from sqlalchemy import CHAR, Boolean, Column
from sqlalchemy.dialects.mysql import ENUM


class Room(Base):  # TODO(high)(SpeedFox198): change disappearing to 3 options (change docs too)
    __tablename__ = "room"

    def __init__(self, disappearing: bool = False, type_: str = "direct"):
        """
        Creates a room object

        Args:
            disappearing(bool): True when disappearing messages is on for room
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
    disappearing = Column(Boolean, default=False)
    type = Column(ENUM("direct", "group"))
