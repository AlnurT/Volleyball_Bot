import logging
import sys

from aiogram.methods import DeleteWebhook

from src.base.bot import BOT, DP, SCHEDULER
from src.handlers import make_poll, callback, message
from src.utils.commands import set_main_menu


async def main() -> None:
    """
    Ядро бота для регистрации хэндлеров, расписания и логирования операций
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - "
               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
        stream=sys.stdout,
    )
    await set_main_menu(BOT)

    SCHEDULER.start()
    callback.register_callback_query()
    message.register_message()

    SCHEDULER.add_job(
        make_poll.start_poll,
        trigger="cron",
        day_of_week="sun",
        hour=18,
    )

    try:
        await BOT(DeleteWebhook(drop_pending_updates=True))
        await DP.start_polling(BOT)
    finally:
        await BOT.session.close()
