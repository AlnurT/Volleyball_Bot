from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.formatting import as_list, as_numbered_list

from src.bot_base import dp
from src.core.database.orm import AsyncOrm
from src.core.keyboards.inline import get_inline_keyboard


def send_text(players_list, not_players_list):
    if not players_list:
        players_list = [""]

    if not not_players_list:
        not_players_list = [""]

    return as_list(
        "Игра в четверг\n",
        "Участники:",
        as_numbered_list(*players_list, fmt="{}.    "),
        "",
        as_numbered_list(*not_players_list, fmt="{}.    "),
    )


def create_player_tables(players=None):
    players_list, not_players_list = [], []

    for pl in players:
        if pl.is_play:
            players_list.append(pl.user_name)
        else:
            not_players_list.append(pl.user_name)

        if pl.extra_player > 0:
            players_list.extend([f"{pl.user_name} +1"] * pl.extra_player)

    return players_list, not_players_list


async def test_func():
    # await AsyncOrm.add_player(123456789, "Alnur", False, 5)
    # await AsyncOrm.add_player(567891234, "Talga", False, 2)
    # await AsyncOrm.add_player(912345678, "Lena", True, 0)
    # await AsyncOrm.add_player(912567834, "Kamil", False, 0)
    # await AsyncOrm.update_player_status(567891234, is_play=True)
    # await AsyncOrm.update_player_status(123456789, extra_player=1)
    # await AsyncOrm.update_player_status(567891234, extra_player=-1)
    pass


@dp.message(Command("poll"))
async def get_poll(message: Message):
    await AsyncOrm.create_tables()
    text_for_poll = send_text([], [])
    await message.answer(
        **text_for_poll.as_kwargs(),
        reply_markup=get_inline_keyboard(),
    )


# @dp.callback_query()
# async def play_game(call: CallbackQuery):
#     match call.data:
#         case "is_play_true":
#             await call.message.answer("is_play_true")


def register_basic_handlers():
    pass
