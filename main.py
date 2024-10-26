import asyncio
import logging
import os

from aiogram.methods import DeleteWebhook

from src.handlers import message, callback
from src.utils.commands import set_main_menu
from settings import SCHEDULER, BOT, DP


async def main() -> None:
    """Запуск бота"""

    logging.basicConfig(
        filename=os.path.abspath("logs/bot.log"),
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - "
               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
    )
    await set_main_menu(BOT)

    SCHEDULER.start()
    callback.register_callback_query()
    message.register_message()

    try:
        await BOT(DeleteWebhook(drop_pending_updates=True))
        await DP.start_polling(BOT)
    finally:
        await BOT.session.close()


if __name__ == "__main__":
    asyncio.run(main())
