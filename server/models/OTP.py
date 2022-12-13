from uuid import uuid4

from sqlalchemy import (
    Column,
    CHAR,
    INTEGER,
    VARCHAR
)

from models import User

from db_access.globals import Base

class OTP (Base):
    __tablename__ = "OTP"

    def __init__ (self, email, otp, password):
        self.email = email
        self.otp = otp
        self.password = password

    email = Column(VARCHAR(255), unique=True, nullable=False)
    otp = Column(INTEGER(6), nullable=False)
    password = Column(CHAR(64), nullable=False)