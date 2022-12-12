from uuid import uuid4

from sqlalchemy import (
    Column,
    CHAR,
    Integer
)
from db_access.globals import Base

class Timeout (Base):
    __tablename__ = "Timeout"

    def __init__ (self, user_id, timeout):
        self.user_id = user_id
        self.timeout = timeout

    user_id = Column(CHAR(36), primary_key=True)
    timeout = Column(Integer, default=False)