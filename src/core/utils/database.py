import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import settings

async_engine = create_async_engine(
    url=settings.database_url_asyncpg,
    echo=False,
)


async def async_engine_connect():
    async with async_engine.connect() as conn:
        res = await conn.execute(text("SELECT VERSION()"))
        print(f"{res.all()=}")


asyncio.run(async_engine_connect())
