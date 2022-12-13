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

    def __init__ (self, user_id, otp, password):
        self.user_id = user_id
        self.otp = otp
        self.password = password

    user_id = Column(CHAR(36), ForeignKey(User.user_id), primary_key=True)
    otp = Column(INTEGER(6), nullable=False)
    password = Column(CHAR(64), nullable=False)