from aiogram.filters import Command
from aiogram.types import Message

from src.base.bot import DP, BOT

from src.keyboards.inline import get_action_keyboard


@DP.message(Command("action"))
async def get_admin_keyboard(message: Message) -> None:
    """
    Создать новый или старый опрос админом

    :param message: Сообщение пользователя
    """
    await message.delete()
    await BOT.send_message(
        chat_id=message.chat.id,
        text="Выбор действия",
        reply_markup=get_action_keyboard()
    )


def register_message() -> None:
    """Регистрация ответов на сообщения"""
    pass