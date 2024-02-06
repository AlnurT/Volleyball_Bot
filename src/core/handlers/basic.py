from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.formatting import as_list, as_numbered_list

from src.bot_base import dp
from src.core.database.orm import AsyncOrm
from src.core.keyboards.inline import get_inline_keyboard


async def send_text():
    players = await AsyncOrm.get_players_list()
    not_players = await AsyncOrm.get_not_players_list()
    players_name_list = [
        pl.user_name if pl.is_play else f"{pl.user_name} +1" for pl in players
    ]
    not_players_name_list = [pl.user_name for pl in not_players]

    return as_list(
        "Игра в четверг\n",
        "Участники:",
        as_numbered_list(*players_name_list, fmt="{}.    "),
        "",
        as_numbered_list(*not_players_name_list, fmt="{}.    "),
    )


async def test_func():
    await AsyncOrm.add_player(123456789, "Alnur", False, 5)
    await AsyncOrm.add_player(567891234, "Talga", False, 2)
    await AsyncOrm.add_player(912345678, "Lena", True, 0)
    await AsyncOrm.add_player(912567834, "Kamil", False, 0)
    await AsyncOrm.update_player_status(567891234, is_play=True)
    await AsyncOrm.update_player_status(123456789, extra_player=1)
    await AsyncOrm.update_player_status(567891234, extra_player=-1)


@dp.message(Command("poll"))
async def get_poll(message: Message):
    await AsyncOrm.create_tables()
    await test_func()
    text_for_poll = await send_text()
    await message.answer(
        **text_for_poll.as_kwargs(),
        reply_markup=get_inline_keyboard(),
    )


# @dp.callback_query()
# async def play_game(call: CallbackQuery):
#     if call.data == "is_play_true":
#         await call.message.answer("Ar")


def register_basic_handlers():
    pass
