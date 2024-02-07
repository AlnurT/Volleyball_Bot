from sqlalchemy import select

from src.core.database.db_base import Base, async_engine, async_session_factory
from src.core.database.models import PlayersOrm


class AsyncOrm:
    players_list: list = []

    async def get_players_list(self):
        async with async_session_factory() as session:
            query = select(PlayersOrm)
            result = await session.execute(query)
            self.players_list = result.scalars().all()

    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def update_player_status(
        user_id: int, is_play: bool = False, extra_player: int = 0
    ):
        async with async_session_factory() as session:
            player = await session.get(PlayersOrm, user_id)
            if extra_player:
                player.extra_pl += extra_player
            else:
                player.is_play = is_play
            await session.commit()

    @staticmethod
    async def add_player(user_id: int, user_name: str, is_play: bool, extra_pl: int):
        players = PlayersOrm(
            user_id=user_id, user_name=user_name, is_play=is_play, extra_pl=extra_pl
        )
        async with async_session_factory() as session:
            session.add(players)
            await session.commit()
