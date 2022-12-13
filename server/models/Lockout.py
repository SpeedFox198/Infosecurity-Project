from datetime import datetime
from models import User

from sqlalchemy import (
    Column,
    CHAR,
    TIMESTAMP,
    ForeignKey
)
from db_access.globals import Base

class Lockout (Base):
    __tablename__ = "Lockout"

    def __init__ (self, user_id):
        self.user_id = user_id
        self.lockout = datetime.now()

    user_id = Column(CHAR(36), ForeignKey(User.user_id), primary_key=True)
    lockout = Column(TIMESTAMP())