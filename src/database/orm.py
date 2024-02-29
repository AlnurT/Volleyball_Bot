from aiogram.utils.markdown import hlink
from sqlalchemy import desc, select

from src.database.db_base import Base, async_engine, async_session_factory
from src.database.models import PlayersOrm


class AsyncOrm:
    @staticmethod
    async def get_players_list(is_play: bool):
        async with async_session_factory() as session:
            query = select(PlayersOrm).filter_by(is_play=is_play)
            res = await session.execute(query)
            result = res.scalars().all()
            if not result:
                return [""]
            return (hlink(pl.user_name, f"tg://user?id={pl.user_id}") for pl in result)

    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def update_pl_status(user_id: int, user_name: str, is_play: bool):
        async with async_session_factory() as session:
            query = select(PlayersOrm).filter_by(user_id=user_id, user_name=user_name)
            res = await session.execute(query)
            result = res.scalars().first()

            if not result:
                player = PlayersOrm(
                    user_id=user_id,
                    user_name=user_name,
                    is_play=is_play,
                )
                session.add(player)
                await session.commit()
                return True

            if result.is_play is is_play:
                return False

            result.is_play = is_play
            await session.commit()
            return True

    @staticmethod
    async def update_extra_pl(user_id: int, user_name: str, extra_pl: int):
        async with async_session_factory() as session:
            if extra_pl == 1:
                player = PlayersOrm(
                    user_id=user_id, user_name=f"{user_name} +1", is_play=True
                )
                session.add(player)
                await session.commit()
                return True

            query = (
                select(PlayersOrm)
                .filter_by(user_id=user_id, user_name=f"{user_name} +1")
                .order_by(desc(PlayersOrm.id_num))
            )
            res = await session.execute(query)
            result = res.scalars().first()
            if result is None:
                return False

            await session.delete(result)
            await session.commit()
            return True
