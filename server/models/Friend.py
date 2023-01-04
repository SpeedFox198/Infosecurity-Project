from sqlalchemy import (
    Column,
    CHAR, ForeignKey
)

from db_access.globals import Base
from models import User


class Friend(Base):
    __tablename__ = "friend"

    def __init__(self, user1_id: str, user2_id: str) -> None:
        self.user1_id = user1_id
        self.user2_id = user2_id

    user1_id = Column(CHAR(36), ForeignKey(User.user_id), primary_key=True)
    user2_id = Column(CHAR(36), ForeignKey(User.user_id), primary_key=True)
