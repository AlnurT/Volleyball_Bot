from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.formatting import as_list, as_numbered_list

from src.bot_base import dp
from src.core.keyboards.inline import get_inline_keyboard


@dp.message(Command("poll"))
async def get_pool(message: Message):
    text = as_list(
        "Игра в четверг\n",
        "Участники:",
        as_numbered_list(*["Alnur", "Talga", "Lena"], fmt="{}.    "),
    )
    await message.answer(
        **text.as_kwargs(),
        reply_markup=get_inline_keyboard(),
    )


def register_basic_handlers():
    pass
