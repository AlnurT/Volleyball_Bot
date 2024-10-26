from aiogram import F
from aiogram.types import CallbackQuery

from settings import DP
from bot.database.orm import VlPlayersOrm
from bot.utils.poll_action import start_poll
from bot.utils.poll_text import TextPoll
from bot.keyboards.inline import get_poll_keyboard


@DP.callback_query(F.data.in_({"new", "old"}))
async def create_poll(call: CallbackQuery) -> None:
    """Ручной запуск опроса"""

    await start_poll(call.data)
    await call.message.delete()


@DP.callback_query(F.data.in_({"play", "not_play", "plus", "minus"}))
async def play_game(call: CallbackQuery) -> None:
    """Изменение списков опроса при нажатии на кнопки

    - play: добавить себя в список
    - not_play: удалить себя из списка
    - plus: добавить гостя в список
    - minus: удалить гостя из списка
    """

    user = call.from_user
    user_id = str(user.id)
    is_change = False

    match call.data:
        case "play":
            name = user.full_name
            is_change = await VlPlayersOrm.add_player(user_id, name, "player")

        case "plus":
            name = user.first_name
            is_change = await VlPlayersOrm.add_player(user_id, name, "guest")

        case "not_play":
            is_change = await VlPlayersOrm.remove_player(user_id, "player")

        case "minus":
            is_change = await VlPlayersOrm.remove_player(user_id, "guest")

    if not is_change:
        return

    players = await VlPlayersOrm.get_players()
    text_for_poll = TextPoll.send_poll(players)

    await call.message.edit_caption(
        caption=text_for_poll, reply_markup=get_poll_keyboard()
    )


def register_callback_query() -> None:
    """Регистрация ответов на нажатие кнопок"""
    pass
