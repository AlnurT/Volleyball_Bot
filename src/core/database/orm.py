from src.core.database.db_base import Base, async_engine, async_session_factory
from src.core.database.models import PlayersOrm


class AsyncOrm:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insert_players(
        user_id: int, user_name: str, is_play: bool, extra_pl: int
    ):
        players = PlayersOrm(
            user_id=user_id, user_name=user_name, is_play=is_play, extra_pl=extra_pl
        )
        async with async_session_factory() as session:
            session.add(players)
            await session.commit()
