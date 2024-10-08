import os

from aiogram.enums import ParseMode
from aiogram.types import FSInputFile, Message

from bot.database.orm import VlPlayersOrm
from bot.keyboards.inline import get_poll_keyboard, get_end_keyboard
from bot.utils.poll_text import TextPoll
from config import BOT, SETTINGS, SCHEDULER


async def get_poll() -> None:
    """Создание опроса и расписания конца опроса"""

    players = await VlPlayersOrm.get_players()
    text_for_poll = TextPoll.send_poll(players)

    message = await BOT.send_photo(
        chat_id=SETTINGS.BOT_CHAT_ID,
        photo=FSInputFile(os.path.abspath("bot/images/volleyball.jpg")),
        caption=text_for_poll,
        parse_mode=ParseMode.HTML,
        reply_markup=get_poll_keyboard(),
    )
    SCHEDULER.add_job(
        end_poll,
        trigger="cron",
        day_of_week="tue",
        hour=23,
        kwargs={"message": message},
    )


async def end_poll(message: Message) -> None:
    """
    Удаление кнопок голосования после конца опроса

    :param message: Сообщение опроса
    """
    players = await VlPlayersOrm.get_players()
    text_for_poll = TextPoll.send_poll(players, True)

    await message.edit_caption(
        caption=text_for_poll, reply_markup=get_end_keyboard(),
    )


async def start_poll() -> None:
    """Запустить голосование"""

    await VlPlayersOrm.create_table()
    await get_poll()
