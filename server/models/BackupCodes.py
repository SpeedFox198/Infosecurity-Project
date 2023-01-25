from sqlalchemy import (
    Column,
    VARCHAR,
    CHAR,
    ForeignKey
)

from db_access.globals import Base

from models import User


class BackupCodes(Base):
    # 6 2FA backup Code
    __tablename__ = "backup_codes"

    def __init__(self, user_id, code):
        self.user_id = user_id
        self.code = code

    user_id = Column(CHAR(36), ForeignKey(User.user_id), primary_key=True)
    code = Column(VARCHAR(255), nullable=False, primary_key = True)
