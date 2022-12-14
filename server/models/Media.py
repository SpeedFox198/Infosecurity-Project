from db_access.globals import Base
from models import Message
from sqlalchemy import CHAR, VARCHAR, Column, ForeignKey


class Media(Base):
    __tablename__ = "Media"

    message_id = Column(CHAR(36), ForeignKey(Message.message_id), primary_key=True)
    path = Column(VARCHAR(255))

