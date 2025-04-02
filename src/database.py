from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from src.config import settings
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import NullPool

db_params = {}
if settings.MODE == "TEST":
    db_params = {"poolclass": NullPool}

engine = create_async_engine(settings.DB_URL, **db_params)
engine_null_pool = create_async_engine(settings.DB_URL, poolclass=NullPool)

async_session_maker = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
async_session_maker_null_pool = async_sessionmaker(
    bind=engine_null_pool, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass
