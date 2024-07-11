from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.base.bot import SETTINGS

ASYNC_ENGINE = create_async_engine(
    url=SETTINGS.database_url_asyncpg,
    echo=False,
)

ASYNC_SESSION = async_sessionmaker(ASYNC_ENGINE)


class Base(AsyncAttrs, DeclarativeBase):
    """Класс для создания моделей"""

    pass


class PlayersOrm(Base):
    """Класс для создания таблицы в базе данных"""

    __tablename__ = "players"

    id_num: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str]
    user_name: Mapped[str]
    status: Mapped[int]
