from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.utils.formatting import as_list, as_numbered_list

from src.bot_base import dp
from src.core.database.orm import AsyncOrm
from src.core.keyboards.inline import get_inline_keyboard


async def send_text():
    players_list = await AsyncOrm.get_players_list()
    not_players_list = await AsyncOrm.get_not_players_list()

    return as_list(
        "Игра в четверг\n",
        "Участники:",
        as_numbered_list(*players_list, fmt="{}.    "),
        "",
        "Не играют:",
        as_numbered_list(*not_players_list, fmt="{}.    "),
    )


@dp.message(Command("poll"))
async def get_poll(message: Message):
    await AsyncOrm.create_tables()
    text_for_poll = await send_text()
    await message.answer(
        **text_for_poll.as_kwargs(),
        reply_markup=get_inline_keyboard(),
    )


@dp.callback_query()
async def play_game(call: CallbackQuery):
    user_id = call.from_user.id
    name = call.from_user.first_name
    is_change = False

    match call.data:
        case "is_play_true":
            is_change = await AsyncOrm.update_pl_status(user_id, name, True)
        case "is_play_false":
            is_change = await AsyncOrm.update_pl_status(user_id, name, False)
        case "plus_extra_pl":
            is_change = await AsyncOrm.update_extra_pl(user_id, name, extra_pl=1)
        case "minus_extra_pl":
            is_change = await AsyncOrm.update_extra_pl(user_id, name, extra_pl=-1)

    if is_change:
        text_for_poll = await send_text()
        await call.message.edit_text(**text_for_poll.as_kwargs())
        await call.message.edit_reply_markup(reply_markup=get_inline_keyboard())


def register_basic_handlers():
    pass
