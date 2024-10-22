import asyncio
import logging
import os

from aiogram.methods import DeleteWebhook

from bot.handlers import message, callback
from bot.utils.commands import set_main_menu
from bot.utils.log_action import clear_log
from bot.utils.poll_action import start_poll
from settings import SCHEDULER, BOT, DP


async def main() -> None:
    """
    Ядро бота для регистрации хэндлеров, расписания и логирования операций
    """
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

    SCHEDULER.add_job(
        start_poll,
        trigger="cron",
        day_of_week="sun",
        hour=18,
    )
    SCHEDULER.add_job(
        clear_log,
        trigger="cron",
        day_of_week="sun",
        hour=17,
    )

    try:
        await BOT(DeleteWebhook(drop_pending_updates=True))
        await DP.start_polling(BOT)
    finally:
        await BOT.session.close()


if __name__ == "__main__":
    asyncio.run(main())
