from typing import List

from sqlalchemy import select

from src.database.models import ASYNC_ENGINE, ASYNC_SESSION, Base, PlayersOrm


class VlPlayersOrm:
    """Класс для работы с базой данных"""

    @staticmethod
    async def get_players_list(is_play: bool) -> List[str]:
        """
        Получение списка игроков со ссылкой на аккаунт в телеграмме

        :param is_play: Флаг для списка играющих или неиграющих игроков
        :return: Список игроков
        """
        async with ASYNC_SESSION() as session:
            query = (
                select(PlayersOrm).filter(PlayersOrm.status != 0)
                if is_play
                else select(PlayersOrm).filter(PlayersOrm.status == 0)
            )

            res = await session.execute(query)
            result = res.scalars().all()

            if not result:
                return [""]

            return [
                f"<a href='tg://user?id={pl.user_id}'>{pl.user_name}</a>"
                if pl.status != 2
                else f"Игрок от <a href='tg://user?id={pl.user_id}'>{pl.user_name}</a>"
                for pl in result
            ]

    @staticmethod
    async def create_new_tables() -> None:
        """Очистка и создание таблицы"""
        async with ASYNC_ENGINE.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def update_pl_status(user_id: str, user_name: str, status: int) -> bool:
        """
        Изменение статуса игроков в базе данных

        :param user_id: ID игрока
        :param user_name: Полное имя игрока
        :param status: Статус игрока (0 - нет, 1 - да, 2 - будет гость)
        :return: Флаг для внесения изменений в базу данных
        """
        async with ASYNC_SESSION() as session:
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
    async def update_extra_pl(user_id: str, user_name: str, extra_pl: int) -> bool:
        """
        Изменение статуса гостей в базе данных

        :param user_id: ID игрока
        :param user_name: Полное имя игрока
        :param extra_pl: Количество гостей для добавления(+1) или удаления(-1) в базе данных
        :return: Флаг для внесения изменений в базу данных
        """
        async with ASYNC_SESSION() as session:
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
