from sqlalchemy import Column, VARCHAR, CHAR, ForeignKey

from db_access.globals import Base
from models import User


class SioConnection(Base):
    # Information about the user's socketio data when they connect
    def __init__(self, sid, user_id):
        self.sid = sid
        self.user_id = user_id

    __tablename__ = "sio_connection"

    sid = Column(VARCHAR(255), primary_key=True)
    user_id = Column(CHAR(36), ForeignKey(User.user_id), primary_key=True)
