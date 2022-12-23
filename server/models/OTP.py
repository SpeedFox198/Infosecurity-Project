from sqlalchemy import (
    Column,
    INTEGER,
    VARCHAR
)

from db_access.globals import Base


class OTP(Base):
    __tablename__ = "otp"

    def __init__ (self, email, otp, password):
        self.email = email
        self.otp = otp
        self.password = password

    email = Column(VARCHAR(255), unique=True, nullable=False, primary_key=True)
    otp = Column(INTEGER, nullable=False)
    password = Column(VARCHAR(255), nullable=False)
