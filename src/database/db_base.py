from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.base.bot import SETTINGS

ASYNC_ENGINE = create_async_engine(
    url=SETTINGS.database_url_asyncpg,
    echo=False,
)

ASYNC_SESSION = async_sessionmaker(ASYNC_ENGINE)


class Base(AsyncAttrs, DeclarativeBase):
    pass
