import asyncio
import logging
import sys

from aiogram.methods import DeleteWebhook

from src.bot_base import bot, dp
from src.core.handlers import basic, info


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
        stream=sys.stdout,
    )

    basic.register_basic_handlers()
    info.register_info_handlers()

    try:
        await bot(DeleteWebhook(drop_pending_updates=True))
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
