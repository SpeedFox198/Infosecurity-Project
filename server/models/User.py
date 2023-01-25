from uuid import uuid4

from sqlalchemy import (
    Column,
    VARCHAR,
    CHAR,
    Boolean
)
from sqlalchemy.orm import relationship

from db_access.globals import Base


class User(Base):
    __tablename__ = "user"

    def __init__(self, username, email, password):
        self.user_id = str(uuid4())
        self.username = username
        self.email = email
        self.password = password

    user_id = Column(CHAR(36), primary_key=True)
    username = Column(VARCHAR(32), unique=True, nullable=False)
    email = Column(VARCHAR(255), unique=True, nullable=False)
    password = Column(VARCHAR(255))
    avatar = Column(VARCHAR(255))
    public_key = Column(CHAR(88))
    dark_mode = Column(Boolean, default=False)
    malware_scan = Column(Boolean, default=True)
    friends_only = Column(Boolean, default=True)
    censor = Column(Boolean, default=True)
    google_account = Column(Boolean, default=False)
    twofa_status = Column(Boolean, default=False)
    disappearing = Column(Boolean, default=False)
    online = Column(Boolean)

    devices = relationship("Device", back_populates="user")
