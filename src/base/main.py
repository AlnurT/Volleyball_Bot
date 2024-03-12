import logging
import sys

from aiogram.methods import DeleteWebhook

from src.base.bot import bot, dp, scheduler
from src.handlers import basic
from src.utils import info


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
        stream=sys.stdout,
    )
    scheduler.start()
    basic.register_basic_handlers()
    info.register_info_handlers()

    try:
        await bot(DeleteWebhook(drop_pending_updates=True))
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
