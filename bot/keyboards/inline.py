from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from settings import WEB_URL


def get_poll_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура опроса игроков"""

    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.button(text="Буду играть 👍", callback_data="play")
    keyboard_builder.button(text="Не смогу 👎", callback_data="not_play")
    keyboard_builder.button(text="+1 игрок 🤝", callback_data="plus")
    keyboard_builder.button(text="-1 игрок 🚷", callback_data="minus")
    keyboard_builder.button(text="Подробнее ⚡️", url=WEB_URL)

    keyboard_builder.adjust(2, 2, 1)

    return keyboard_builder.as_markup()


def get_end_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура конца опроса"""

    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Подробнее ⚡️", url=WEB_URL)

    return keyboard_builder.as_markup()


def get_action_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура действий админа"""

    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.button(text="Новый опрос", callback_data="new")
    keyboard_builder.button(text="Старый опрос", callback_data="old")
    keyboard_builder.adjust(2)

    return keyboard_builder.as_markup()
