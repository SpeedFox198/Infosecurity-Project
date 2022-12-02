from server.db_access.globals import Base
from sqlalchemy import (
    Column,
    CHAR,
    VARCHAR,
)


class Media(Base):
    __tablename__ = "Media"

    message_id = Column(CHAR(36), primary_key=True)
    path = Column(VARCHAR(255))

