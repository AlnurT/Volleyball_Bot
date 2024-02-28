from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from src.config import settings

bot = Bot(settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
