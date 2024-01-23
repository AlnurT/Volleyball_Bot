from aiogram.filters import Command
from aiogram.types import Message

from src.bot_base import dp
from src.core.keyboards.inline import get_inline_keyboard
from src.core.utils.dbconnect import Request


async def get_pool(message: Message, request: Request):
    text = "\n".join(x["user_name"] for x in await request.get_data())
    await message.answer(
        f"Привет, {message.from_user.first_name}. Показываю кнопки!\n{text}",
        reply_markup=get_inline_keyboard(),
    )


def register_basic_handlers():
    dp.message.register(get_pool, Command("poll"))


# await request.add_data(
#     user_id=message.from_user.id,
#     user_name=message.from_user.first_name,
#     game=True,
#     extra_players=0,
# )
