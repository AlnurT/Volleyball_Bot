from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from src.bot_base import dp


async def command_start(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


def register_basic_handlers():
    dp.message.register(command_start, CommandStart())
