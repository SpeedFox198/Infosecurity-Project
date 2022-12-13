from sqlalchemy import (
    Column,
    CHAR,
    Text,
    ForeignKey
)

from models import User

from db_access.globals import Base

class TwoFA (Base):
    __tablename__ = "2FA"

    def __init__ (self, user_id, secret):
        self.user_id = user_id
        self.secret = secret

    user_id = Column(CHAR(36), ForeignKey(User.user_id), primary_key=True)
    secret = Column(Text)