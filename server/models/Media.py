from db_access.globals import Base
from models import Message
from sqlalchemy import CHAR, VARCHAR, Column, ForeignKey, INT


class Media(Base):
    __tablename__ = "media"

    def __init__(self, message_id: str, path: str, height: int, width: int):
        self.message_id = message_id
        self.path = path
        self.height = height
        self.width = width

    message_id = Column(CHAR(36), ForeignKey(Message.message_id), primary_key=True)
    path = Column(VARCHAR(255))

    # Display height and width, not actual height and width
    height = Column(INT)
    width = Column(INT)
