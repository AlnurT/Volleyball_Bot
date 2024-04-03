from sqlalchemy import select

from src.database.db_base import Base, async_engine, async_session_factory
from src.database.models import PlayersOrm


class AsyncOrm:
    @staticmethod
    async def get_players_list(is_play: bool):
        async with async_session_factory() as session:
            if is_play:
                query = select(PlayersOrm).filter(PlayersOrm.status != 0)
            else:
                query = select(PlayersOrm).filter(PlayersOrm.status == 0)

            res = await session.execute(query)
            result = res.scalars().all()

            if not result:
                return " "

            return [
                f"<a href='tg://user?id={pl.user_id}'>{pl.user_name}</a>"
                if pl.status != 2
                else f"Игрок от <a href='tg://user?id={pl.user_id}'>{pl.user_name}</a>"
                for pl in result
            ]

    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def update_pl_status(user_id: int, user_name: str, status: int):
        async with async_session_factory() as session:
            query = select(PlayersOrm).filter(
                PlayersOrm.user_id == user_id,
                PlayersOrm.user_name == user_name,
                PlayersOrm.status != 2,
            )
            res = await session.execute(query)
            result = res.scalars().first()

            if not result:
                player = PlayersOrm(
                    user_id=user_id,
                    user_name=user_name,
                    status=status,
                )
                session.add(player)
                await session.commit()
                return True

            if result.status == status:
                return False

            result.status = status
            await session.commit()
            return True

    @staticmethod
    async def update_extra_pl(user_id: int, user_name: str, extra_pl: int):
        async with async_session_factory() as session:
            if extra_pl == 1:
                player = PlayersOrm(user_id=user_id, user_name=user_name, status=2)
                session.add(player)
                await session.commit()
                return True

            query = select(PlayersOrm).filter_by(
                user_id=user_id, user_name=user_name, status=2
            )
            res = await session.execute(query)
            result = res.scalars().first()
            if result is None:
                return False

            await session.delete(result)
            await session.commit()
            return True
