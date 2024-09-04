from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from environs import Env
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class Settings:
    """Класс настройки базы данных и бота"""

    BOT_TOKEN: str
    BOT_ADMIN_ID: int
    BOT_CHAT_ID: int
    PG_HOST: str
    PG_PORT: int
    PG_DB: str
    PG_USER: str
    PG_PASS: str

    @property
    def database_url_asyncpg(self) -> str:
        """Настройка доступа к БД"""
        return f"postgresql+asyncpg://" \
               f"{self.PG_USER}:{self.PG_PASS}" \
               f"@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"

    def get_settings(self, path: str) -> None:
        """
        Привязка переменных бота и БД

        :param path: Путь к данным бота и БД для подключения
        """
        env = Env()
        env.read_env(path)

        self.BOT_TOKEN = env.str("BOT_TOKEN")
        self.BOT_ADMIN_ID = env.int("ADMIN_ID")
        self.BOT_CHAT_ID = env.int("CHAT_ID")
        self.PG_HOST = env.str("POSTGRES_HOST")
        self.PG_PORT = env.str("POSTGRES_PORT")
        self.PG_DB = env.str("POSTGRES_DB")
        self.PG_USER = env.str("POSTGRES_USER")
        self.PG_PASS = env.str("POSTGRES_PASSWORD")


SETTINGS = Settings()
SETTINGS.get_settings(path=".env")

ASYNC_ENGINE = create_async_engine(
    url=SETTINGS.database_url_asyncpg,
    echo=False,
)
ASYNC_SESSION = async_sessionmaker(ASYNC_ENGINE)

SCHEDULER = AsyncIOScheduler(timezone="Europe/Moscow")

BOT = Bot(
    SETTINGS.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
DP = Dispatcher()
