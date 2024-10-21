from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from environs import Env
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")

ADMIN_ID = env.int("ADMIN_ID")
CHAT_ID = env.int("CHAT_ID")

PG_HOST = env.str("PG_HOST")
PG_PORT = env.str("PG_PORT")
PG_DB = env.str("PG_DB")
PG_USER = env.str("PG_USER")
PG_PASS = env.str("PG_PASS")

PG_URL = f"postgresql+asyncpg://" \
         f"{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}"

ASYNC_ENGINE = create_async_engine(url=PG_URL, echo=False)
ASYNC_SESSION = async_sessionmaker(ASYNC_ENGINE)

BOT = Bot(
    BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
DP = Dispatcher()

SCHEDULER = AsyncIOScheduler(timezone="Europe/Moscow")
