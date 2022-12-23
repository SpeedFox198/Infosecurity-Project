from db_access.globals import Base
from sqlalchemy import CHAR, VARCHAR, Column


DEFAULT_ICON_PATH = "/default.png"  # TODO(SpeedFox198): change this in the future


class Group(Base):
    __tablename__ = "group"

    def __init__(self, room_id:str, name:str, icon:str=DEFAULT_ICON_PATH):
        self.room_id = room_id
        self.name = name
        self.icon = icon

    room_id = Column(CHAR(36), primary_key=True)
    name = Column(VARCHAR(25))
    icon = Column(VARCHAR(255))
