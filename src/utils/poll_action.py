import os
from datetime import datetime, timedelta

import pytz
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile, Message, InputMediaPhoto

from src.database.orm import VlPlayersOrm
from src.keyboards.inline import get_poll_keyboard, get_end_keyboard, \
    get_payment_keyboard
from src.utils.mailing_list import send_payment_notification
from src.utils.poll_text import TextPoll
from settings import BOT, SCHEDULER, CHAT_ID, ADMIN_ID


async def get_poll() -> None:
    """Создание опроса и расписания конца опроса и напоминаний об оплате"""

    players = await VlPlayersOrm.get_players()
    text_for_poll = TextPoll.send_poll(players)

    message = await BOT.send_photo(
        chat_id=CHAT_ID,
        photo=FSInputFile(os.path.abspath("src/images/start.jpg")),
        caption=text_for_poll,
        parse_mode=ParseMode.HTML,
        reply_markup=get_poll_keyboard(),
    )

    SCHEDULER.add_job(
        end_poll,
        trigger="date",
        run_date=datetime.now(pytz.timezone("Europe/Moscow")) + timedelta(days=2, hours=5),
        kwargs={"message": message},
    )
    SCHEDULER.add_job(
        send_payment_notification,
        trigger="date",
        run_date=datetime.now(pytz.timezone("Europe/Moscow")) + timedelta(days=5),
    )


async def end_poll(message: Message) -> None:
    """
    После конца опроса:

    - удаление кнопок голосования
    - отправка сообщения админу об изменении статуса оплаты игроков
    """

    players = await VlPlayersOrm.get_players()
    text_for_poll = TextPoll.send_poll(players)

    await message.edit_media(
        InputMediaPhoto(
            media=FSInputFile(os.path.abspath("src/images/end.jpg")),
            caption=text_for_poll,
        ),
        reply_markup=get_end_keyboard(),
    )

    await BOT.send_message(
        chat_id=ADMIN_ID,
        text=TextPoll.send_poll(players, True),
        parse_mode=ParseMode.HTML,
        reply_markup=get_payment_keyboard(players),
    )


async def start_poll(data: str = "new") -> None:
    """Запустить голосование"""

    if data == "new":
        await VlPlayersOrm.create_table()

    await get_poll()
