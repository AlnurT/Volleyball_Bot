from typing import Sequence

from sqlalchemy import select, exists, desc

from src.database.models import PlayersOrm
from settings import ASYNC_ENGINE, ASYNC_SESSION


class VlPlayersOrm:
    """Класс для работы с базой данных"""

    @staticmethod
    async def create_table() -> None:
        """Удаление и создание таблицы"""

        async with ASYNC_ENGINE.begin() as conn:
            await conn.run_sync(PlayersOrm.metadata.drop_all)
            await conn.run_sync(PlayersOrm.metadata.create_all)

    @staticmethod
    async def get_players(is_pay: bool = False) -> Sequence:
        """
        Получение списка игроков со ссылкой на аккаунт в телеграмме

        :param is_pay: Проверка на список с оплатой
        """
        async with ASYNC_SESSION() as session:
            if is_pay:
                query = select(PlayersOrm).filter_by(payment=False).\
                    order_by(PlayersOrm.num)
            else:
                query = select(PlayersOrm).order_by(PlayersOrm.num)

            players = await session.scalars(query)

        return players.all()

    @staticmethod
    async def add_player(user_id: str, name: str, status: str) -> bool:
        """
        Добавление игрока в базу данных

        :param user_id: ID игрока
        :param name: имя игрока
        :param status: статус игрока
        :return: флаг для внесения изменений в базу данных
        """
        async with ASYNC_SESSION() as session:
            player = await session.execute(
                select(exists().where(
                    PlayersOrm.user_id == user_id,
                    PlayersOrm.status == status)
                )
            )

            if player.scalar() and status == "player":
                return False

            session.add(
                PlayersOrm(user_id=user_id, name=name, status=status)
            )
            await session.commit()

        return True

    @staticmethod
    async def remove_player(user_id: str, status: str) -> bool:
        """
        Удаление игрока из базы данных

        :param user_id: ID игрока
        :param status: статус игрока
        :return: флаг для внесения изменений в базу данных
        """
        async with ASYNC_SESSION() as session:
            player = await session.scalar(
                select(PlayersOrm).
                filter_by(user_id=user_id, status=status).
                order_by(desc(PlayersOrm.num))
            )

            if not player:
                return False

            await session.delete(player)
            await session.commit()

        return True

    @staticmethod
    async def change_payment_status_(num: int) -> None:
        """
        Изменение статуса оплаты игрока

        :param num: Номер игрока в базе данных
        """
        async with ASYNC_SESSION() as session:
            player = await session.get(PlayersOrm, num)
            player.payment = not player.payment

            await session.commit()
