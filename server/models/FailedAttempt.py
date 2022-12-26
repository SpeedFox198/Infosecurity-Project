from sqlalchemy import (
    Column,
    CHAR,
    INTEGER,
    ForeignKey
)

from models import User

from db_access.globals import Base

class FailedAttempt (Base):
    __tablename__ = "failed_attempt"

    def __init__ (self, user_id, attempts):
        self.user_id = user_id
        self.attempts = attempts

    user_id = Column(CHAR(36), ForeignKey(User.user_id), primary_key=True)
    attempts = Column(INTEGER)
