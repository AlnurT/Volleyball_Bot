from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.utils.config import Settings

SETTINGS = Settings()
SETTINGS.get_settings("utils/.env")

BOT = Bot(SETTINGS.BOT_TOKEN, parse_mode=ParseMode.HTML)
DP = Dispatcher()

SCHEDULER = AsyncIOScheduler(timezone="Europe/Moscow")
