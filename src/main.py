import asyncio
import logging
import sys

from aiogram.methods import DeleteWebhook

from src.bot_base import bot, dp
from src.core.database.orm import AsyncOrm
from src.core.handlers import basic, info


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
        stream=sys.stdout,
    )
    class_async = AsyncOrm()
    await class_async.create_tables()
    await class_async.add_player(123456789, "Alnur", True, 5)
    await class_async.add_player(567891234, "Talga", True, 2)
    await class_async.update_player_status(567891234, is_play=False)
    await class_async.update_player_status(123456789, extra_player=1)
    await class_async.update_player_status(567891234, extra_player=-1)
    await class_async.update_players_list()
    print([x.user_name for x in class_async.players_list])

    basic.register_basic_handlers()
    info.register_info_handlers()

    try:
        await bot(DeleteWebhook(drop_pending_updates=True))
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
