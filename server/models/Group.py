from db_access.globals import Base
from sqlalchemy import CHAR, VARCHAR, Column, ForeignKey

from models import Room

DEFAULT_ICON_PATH = "/default.png"  # TODO(medium)(SpeedFox198): change this in the future


class Group(Base):
    __tablename__ = "group"

    def __init__(self, room_id: str, name: str, icon: str = DEFAULT_ICON_PATH):
        self.room_id = room_id
        self.name = name
        self.icon = icon

    room_id = Column(CHAR(36), ForeignKey(Room.room_id), primary_key=True)
    name = Column(VARCHAR(25))
    icon = Column(VARCHAR(255))
