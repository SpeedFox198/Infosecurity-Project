from sqlalchemy import (
    Column,
    CHAR, ForeignKey
)

from db_access.globals import Base
from models import User


class FriendRequest(Base):
    def __init__(self, sender: str, recipient: str):
        self.sender = sender
        self.recipient = recipient

    __tablename__ = "friend_request"

    sender = Column(CHAR(36), ForeignKey(User.user_id), primary_key=True)
    recipient = Column(CHAR(36), ForeignKey(User.user_id), primary_key=True)
