from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from os import getenv

DB_USERNAME = getenv("DB_USERNAME") or "bubbles"
DB_PASSWORD = getenv("DB_PASSWORD") or "bubbles"
DB_ENDPOINT = getenv("DB_ENDPOINT") or "localhost"

Base = declarative_base()
connection_string = f"mysql+asyncmy://{DB_USERNAME}:{DB_PASSWORD}@{DB_ENDPOINT}:3306/bubbles"

# echo is for debug
engine = create_async_engine(connection_string, echo=False)

# expire_on_commit allows us to use attributes even after commit
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
