from sqlalchemy import (
    Column,
    CHAR,
    TIMESTAMP,
    VARCHAR,
    ForeignKey
)
from sqlalchemy.orm import relationship

from db_access.globals import Base
from models import User


class Device(Base):
    __tablename__ = "Device"

    device_id = Column(CHAR(36), primary_key=True)
    user_id = Column(CHAR(36), ForeignKey(User.user_id), primary_key=True)
    time = Column(TIMESTAMP)
    location = Column(VARCHAR(255))
    os = Column(VARCHAR(255))
    browser = Column(VARCHAR(255))

    user = relationship("User", back_populates="devices")
