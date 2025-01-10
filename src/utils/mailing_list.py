from aiogram.enums import ParseMode

from settings import BOT
from src.database.orm import VlPlayersOrm


def send_message(status: str) -> str:
    if status == "player":
        return "Добрый вечер!\n" \
               "Напоминаю об оплате за предыдущую игру во вторник!"

    return "Добрый вечер!\n" \
           "Напоминаю об оплате вашего гостя за предыдущую игру во вторник!"


async def send_payment_notification() -> None:
    """Напоминание игрокам об оплате"""

    players = await VlPlayersOrm.get_players(is_pay=True)

    for pl in players:

        await BOT.send_message(
            chat_id=int(pl.user_id),
            text=send_message(pl.status),
            parse_mode=ParseMode.HTML,
        )
