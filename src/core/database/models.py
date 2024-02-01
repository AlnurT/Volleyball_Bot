from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.db_base import Base


class PlayersOrm(Base):
    __tablename__ = "players"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str]
    is_play: Mapped[bool | None]
    extra_pl: Mapped[int] = mapped_column(default=0)
