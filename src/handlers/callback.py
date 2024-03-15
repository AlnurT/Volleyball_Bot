from datetime import datetime

from aiogram import F
from aiogram.types import CallbackQuery

from src.base.bot import bot, dp, scheduler
from src.database.orm import AsyncOrm
from src.handlers.basic import get_poll
from src.handlers.poll_text import send_text
from src.keyboards.inline import get_poll_keyboard


@dp.callback_query(F.data.in_({"new_poll", "old_poll", "end_poll"}))
async def restore_poll(call: CallbackQuery):
    is_new_data = True if call.data == "new_poll" else False
    is_game = False if call.data == "end_poll" else True
    await call.message.delete()

    scheduler.add_job(
        get_poll,
        trigger="date",
        run_date=datetime.now(),
        kwargs={"chat_bot": bot, "is_new_data": is_new_data, "is_game": is_game},
    )


@dp.callback_query()
async def play_game(call: CallbackQuery):
    user_id = call.from_user.id
    name = call.from_user.full_name

    if call.data in ("is_play_true", "is_play_false"):
        is_game = True if call.data == "is_play_true" else False
        is_change = await AsyncOrm.update_pl_status(user_id, name, is_game)
    else:
        extra_pl = 1 if call.data == "plus_extra_pl" else -1
        is_change = await AsyncOrm.update_extra_pl(user_id, name, extra_pl=extra_pl)

    if is_change:
        text_for_poll = await send_text()
        await call.message.edit_caption(
            caption=text_for_poll.render()[0], reply_markup=get_poll_keyboard()
        )


def register_callback_query_handlers():
    pass
