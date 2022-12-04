from db_access.globals import Base
from sqlalchemy import (
    Column,
    CHAR,
    VARCHAR
)


class Group(Base):
    __tablename__ = "Group"

    room_id = Column(CHAR(36), primary_key=True)
    name = Column(VARCHAR(25))
    icon = Column(VARCHAR(255))

