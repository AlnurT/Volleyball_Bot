from aiogram.filters import Command
from aiogram.types import Message

from src.bot_base import dp
from src.core.keyboards.inline import get_inline_keyboard


async def get_inline(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}. Показываю кнопки!",
        reply_markup=get_inline_keyboard(),
    )


def register_basic_handlers():
    dp.message.register(get_inline, Command("poll"))
