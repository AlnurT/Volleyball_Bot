from aiogram import Bot
from aiogram.filters import Command
from aiogram.types import Message

from src.base.bot import dp

# async def start_bot(bot: Bot):
#     await bot.send_message(chat_id=836876955, text="Бот запущен!")
#
#
# async def stop_bot(bot: Bot):
#     await bot.send_message(chat_id=836876955, text="Бот остановлен!")


@dp.message(Command("rules"))
async def send_rules(message: Message, bot: Bot):
    rules_path = r"utils\rules.txt"
    with open(rules_path, "r", encoding="utf-8") as rules:
        await bot.send_message(chat_id=message.from_user.id, text=rules.read())


@dp.message()
async def echo(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


def register_info_handlers():
    # dp.startup.register(start_bot)
    # dp.shutdown.register(stop_bot)
    pass
