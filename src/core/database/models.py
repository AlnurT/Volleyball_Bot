from sqlalchemy.orm import Mapped, mapped_column

from src.core.database.db_base import Base


class PlayersOrm(Base):
    __tablename__ = "players"

    id_num: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    user_name: Mapped[str]
    is_play: Mapped[bool | None] = mapped_column(default=None)
