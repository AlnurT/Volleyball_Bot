import asyncpg
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from src.config import settings


async def create_pool():
    return await asyncpg.create_pool(
        user=settings.bots.user,
        password=settings.bots.password,
        database=settings.bots.database,
        host=settings.bots.host,
        port=settings.bots.port,
        command_timeout="60",
    )


bot = Bot(settings.bots.bot_token, parse_mode=ParseMode.HTML)
dp = Dispatcher()
