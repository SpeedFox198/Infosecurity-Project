from uuid import uuid4

from sqlalchemy import (
    Column,
    CHAR,
    INTEGER,
    ForeignKey
)

from models import User

from db_access.globals import Base

class OTP (Base):
    __tablename__ = "OTP"

    def __init__ (self, user_id, otp):
        self.user_id = user_id
        self.otp = otp

    user_id = Column(CHAR(36), ForeignKey(User.user_id), primary_key=True)
    otp = Column(INTEGER(6), nullable=False)