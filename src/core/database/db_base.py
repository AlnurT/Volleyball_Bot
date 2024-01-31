from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

async_engine = create_async_engine(
    url=settings.database_url_asyncpg,
    echo=False,
)

async_session_factory = async_sessionmaker(async_engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass
