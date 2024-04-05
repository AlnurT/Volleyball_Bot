from aiogram import Bot

from src.base.bot import DP, SETTINGS


async def start_bot(bot: Bot) -> None:
    await bot.send_message(chat_id=SETTINGS.BOT_ADMIN_ID, text="Бот запущен!")


async def stop_bot(bot: Bot) -> None:
    await bot.send_message(chat_id=SETTINGS.BOT_ADMIN_ID, text="Бот остановлен!")


def register_info_handlers() -> None:
    DP.startup.register(start_bot)
    DP.shutdown.register(stop_bot)
