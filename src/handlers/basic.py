from datetime import datetime

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message

from src.base.bot import bot, dp, scheduler
from src.config import settings
from src.database.orm import AsyncOrm
from src.handlers.poll_text import send_text
from src.keyboards.inline import get_keyboard_tables, get_poll_keyboard


@dp.message(Command("poll"))
async def get_poll_manually(message: Message):
    message_id = message.from_user.id
    await message.delete()

    if message_id == settings.BOT_ADMIN_ID:
        await message.answer(
            text="Какой опрос восстановить?",
            reply_markup=get_keyboard_tables(),
        )


async def get_poll(chat_bot: Bot, is_new_data: bool):
    if is_new_data:
        await AsyncOrm.create_tables()

    text_for_poll = await send_text()
    message = await chat_bot.send_photo(
        chat_id=settings.BOT_CHAT_ID,
        photo=FSInputFile("utils/volleyball.jpg"),
        caption=text_for_poll.render()[0],
        parse_mode=ParseMode.HTML,
        reply_markup=get_poll_keyboard(),
    )
    scheduler.add_job(
        end_poll,
        trigger="cron",
        hour=datetime.now().hour,
        minute=datetime.now().minute + 1,
        start_date=datetime.now(),
        kwargs={"message": message},
    )


async def end_poll(message: Message):
    text_for_poll = await send_text(False)
    await message.edit_caption(caption=text_for_poll.render()[0])


def register_basic_handlers():
    scheduler.add_job(
        get_poll,
        trigger="cron",
        hour=datetime.now().hour,
        minute=datetime.now().minute,
        second=datetime.now().second + 5,
        start_date=datetime.now(),
        kwargs={"chat_bot": bot, "is_new_data": True},
    )
