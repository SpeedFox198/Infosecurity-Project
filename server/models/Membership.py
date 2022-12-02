from sqlalchemy import (
    Column,
    CHAR,
    Boolean,
    ForeignKey
)

from db_access.globals import Base
from models import Room, User


class Membership(Base):
    __tablename__ = "Membership"

    room_id = Column(CHAR(36), ForeignKey(Room.room_id), primary_key=True)
    user_id = Column(CHAR(36), ForeignKey(User.user_id), primary_key=True)
    is_admin = Column(Boolean)
