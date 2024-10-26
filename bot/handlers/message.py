from aiogram.filters import Command
from aiogram.types import Message

from bot.keyboards.inline import get_action_keyboard
from bot.utils.log_action import clear_log
from bot.utils.poll_action import start_poll
from settings import BOT, DP, ADMIN_ID, SCHEDULER


@DP.message(Command("start"))
async def get_admin_keyboard(message: Message) -> None:
    """Запуск бота по расписанию"""

    if message.from_user.id != ADMIN_ID:
        return

    await message.delete()
    SCHEDULER.add_job(
        start_poll,
        trigger="cron",
        day_of_week="sun",
        hour=18,
    )
    SCHEDULER.add_job(
        clear_log,
        trigger="cron",
        day_of_week="sun",
        hour=17,
    )


@DP.message(Command("action"))
async def get_admin_keyboard(message: Message) -> None:
    """Выбор опроса с новыми или старыми данными"""

    if message.from_user.id != ADMIN_ID:
        return

    await message.delete()
    await BOT.send_message(
        chat_id=message.chat.id,
        text="Выбор действия",
        reply_markup=get_action_keyboard()
    )


def register_message() -> None:
    """Регистрация ответов на сообщения"""
    pass
