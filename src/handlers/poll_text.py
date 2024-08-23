from datetime import datetime
from typing import Sequence, Generator

from aiogram.utils.formatting import as_list


class TextPoll:
    @staticmethod
    def _get_players_gen(players: Sequence) -> Generator:
        """Вывод списка игроков со ссылками на их аккаунт"""

        for index, pl in enumerate(players, 1):
            text = f"<a href='tg://user?id={pl.user_id}'>{pl.name}</a>"
            if pl.status == "player":
                yield f"<code>  {index:>2}. </code> {text}"
            else:
                yield f"<code>  {index:>2}. </code> Игрок от {text}"

    @staticmethod
    def _pure_poll() -> str:
        """Вывод текста без участников"""

        return as_list(
            "🏐 <b>Игра во вторник</b> 🏐\n",
            "👫 Участников нет ...",
        ).render()[0]

    @classmethod
    def _poll(cls, pl: Sequence) -> str:
        """Вывод текста с участниками"""

        players_text = cls._get_players_gen(pl)
        info = f"\n😊   Будет игра {(len(pl) + 1) // 2} на {len(pl) // 2}" \
            if len(pl) >= 8 else "\n😓   Недостаточно игроков"

        return as_list(
            "🏐 <b>Игра во вторник</b>\n",
            "👫 Участники:",
            as_list(*players_text),
            info,
        ).render()[0]

    @classmethod
    def _poll_with_reserve(cls, pl: Sequence) -> str:
        """Вывод текста с участниками и резервом"""

        players_gen = cls._get_players_gen(pl[:14])
        reserve_gen = cls._get_players_gen(pl[14:])

        return as_list(
            "🏐 <b>Игра во вторник</b>\n",
            "👫 Участники:",
            as_list(*players_gen),
            "\n⏳ Резерв:",
            as_list(*reserve_gen),
            f"\n😊   Будет игра 7 на 7",
        ).render()[0]

    @classmethod
    def _end_poll(cls, pl: Sequence) -> str:
        """Вывод текста конца голосования"""

        players_gen = cls._get_players_gen(pl)
        day = datetime.now().strftime("%d.%m")

        return as_list(
            "🏁 <b>Игра завершена</b>\n",
            f"Вторник - {day}\n",
            "👫 Участники:",
            as_list(*players_gen),
            "\n🏆   Всем спасибо за игру!",
        ).render()[0]

    @classmethod
    def send_poll(cls, pl: Sequence, is_end: bool = False) -> str:
        """Вывод текста в зависимости от условий"""
        if not pl:
            return cls._pure_poll()

        if is_end:
            return cls._end_poll(pl[:14])

        if len(pl) <= 14:
            return cls._poll(pl)

        return cls._poll_with_reserve(pl)


