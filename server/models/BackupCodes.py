from sqlalchemy import (
    Column,
    INTEGER,
    VARCHAR
)

from db_access.globals import Base

#6 2FA backup Code
class BackupCodes(Base):
    __tablename__ = "backup_codes"

    def __init__ (self, user_id, code1 , code2 , code3 , code4 , code5 , code6):
        self.user_id = user_id
        self.code1 = code1
        self.code2 = code2
        self.code3 = code3
        self.code4 = code4
        self.code5 = code5
        self.code6 = code6

    user_id = Column(INTEGER, nullable=False, primary_key=True)
    code1 = Column(VARCHAR(255), nullable=False)
    code2 = Column(VARCHAR(255), nullable=False)
    code3 = Column(VARCHAR(255), nullable=False)
    code4 = Column(VARCHAR(255), nullable=False)
    code5 = Column(VARCHAR(255), nullable=False)
    code6 = Column(VARCHAR(255), nullable=False)
