from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message

from src.base.bot import BOT, DP, SCHEDULER, SETTINGS
from src.database.orm import AsyncOrm
from src.handlers.poll_text import send_end_of_poll, send_poll
from src.keyboards.inline import get_keyboard_tables, get_poll_keyboard


@DP.message(Command("poll"))
async def get_poll_manually(message: Message) -> None:
    message_id = message.from_user.id
    await message.delete()

    if message_id == SETTINGS.BOT_ADMIN_ID:
        await message.answer(
            text="Какой опрос восстановить?",
            reply_markup=get_keyboard_tables(),
        )


async def get_poll(
    chat_bot: Bot, is_new_data: bool = True, is_game: bool = True
) -> None:
    if is_new_data:
        await AsyncOrm.create_tables()

    text_for_poll = await send_poll()
    keyboard = get_poll_keyboard() if is_game else None

    message = await chat_bot.send_photo(
        chat_id=SETTINGS.BOT_CHAT_ID,
        photo=FSInputFile("utils/volleyball.jpg"),
        caption=text_for_poll.render()[0],
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard,
    )

    if is_game:
        SCHEDULER.add_job(
            end_poll,
            trigger="cron",
            day_of_week=1,
            hour=21,
            kwargs={"message": message},
        )


async def end_poll(message: Message) -> None:
    text_for_poll = await send_end_of_poll()
    await message.edit_caption(caption=text_for_poll.render()[0])


def register_basic_handlers() -> None:
    SCHEDULER.add_job(
        get_poll,
        trigger="cron",
        day_of_week=0,
        hour=18,
        kwargs={"chat_bot": BOT},
    )
