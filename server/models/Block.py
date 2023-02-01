from db_access.globals import Base
from models import Room, User
from sqlalchemy import CHAR, Column, ForeignKey


class Block(Base):
    __tablename__ = "block"

    def __init__(self, user_id: str, block_id: str, room_id: str):
        self.user_id = user_id
        self.block_id = block_id
        self.room_id = room_id

    user_id = Column(CHAR(36), ForeignKey(User.user_id), primary_key=True)
    block_id = Column(CHAR(36), ForeignKey(User.user_id), primary_key=True)
    room_id = Column(CHAR(36), ForeignKey(Room.room_id), primary_key=True)
