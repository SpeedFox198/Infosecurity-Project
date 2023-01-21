from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
connection_string = "mysql+asyncmy://bubbles:bubbles@localhost:3306/bubbles"

# echo is for debug
engine = create_async_engine(connection_string, echo=False)

# expire_on_commit allows us to use attributes even after commit
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
