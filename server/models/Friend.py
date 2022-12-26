from sqlalchemy import (
    Column,
    CHAR, ForeignKey
)

from db_access.globals import Base
from models import User


class Friend(Base):
    __tablename__ = "friend"

    user1_id = Column(CHAR(36), ForeignKey(User.user_id), primary_key=True)
    user2_id = Column(CHAR(36), ForeignKey(User.user_id), primary_key=True)
