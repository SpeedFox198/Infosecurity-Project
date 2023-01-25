from sqlalchemy import (
    Column,
    CHAR,
    Boolean,
    ForeignKey
)

from db_access.globals import Base
from models import Room, User


class Membership(Base):
    __tablename__ = "membership"

    def __init__(self, room_id: str, user_id: str, is_admin: bool = False):
        self.room_id = room_id
        self.user_id = user_id
        self.is_admin = is_admin

    room_id = Column(CHAR(36), ForeignKey(Room.room_id), primary_key=True)
    user_id = Column(CHAR(36), ForeignKey(User.user_id), primary_key=True)
    is_admin = Column(Boolean, default=False)