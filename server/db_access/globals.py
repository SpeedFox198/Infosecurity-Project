from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
connection_string = "mysql+asyncmy://bubbles:bubbles@localhost:3306/bubbles"
engine = create_async_engine(connection_string, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession)
