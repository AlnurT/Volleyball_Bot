from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.config import settings

bot = Bot(settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
