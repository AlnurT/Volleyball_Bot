import logging
import sys

from aiogram.methods import DeleteWebhook

from src.base.bot import BOT, DP, SCHEDULER
from src.handlers import basic, callback, info


async def main() -> None:
    """Ядро бота для регистрации хэндлеров, расписания и логирования операций"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
        stream=sys.stdout,
    )
    SCHEDULER.start()

    basic.register_basic_handlers()
    info.register_info_handlers()
    callback.register_callback_query_handlers()

    try:
        await BOT(DeleteWebhook(drop_pending_updates=True))
        await DP.start_polling(BOT)
    finally:
        await BOT.session.close()
