from typing import Annotated

from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


str_128 = Annotated[str, 128]
str_50 = Annotated[str, 50]


class Base(AsyncAttrs, DeclarativeBase):
    """Класс для создания моделей"""

    type_annotation_map = {
        str_128: String(128),
        str_50: String(50)
    }
    pass


class PlayersOrm(Base):
    """Класс для создания таблицы в базе данных"""

    __tablename__ = "players"

    num: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str_50]
    name: Mapped[str_128]
    status: Mapped[str_50]
