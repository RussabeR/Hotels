from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from src.config import settings
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(settings.DB_URL)

async_session_maker = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
