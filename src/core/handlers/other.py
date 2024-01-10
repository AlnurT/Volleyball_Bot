from aiogram import types

from src.bot_base import dp


async def echo(message: types.Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


def register_other_handlers():
    dp.message.register(echo)
