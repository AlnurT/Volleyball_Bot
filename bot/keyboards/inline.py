from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_poll_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура опроса игроков

    :return: Клавиатура в сообщении
    """
    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.button(text="Буду играть 👍", callback_data="play")
    keyboard_builder.button(text="Не смогу 👎", callback_data="not_play")
    keyboard_builder.button(text="+1 игрок 🤝", callback_data="plus")
    keyboard_builder.button(text="-1 игрок 🚷", callback_data="minus")
    keyboard_builder.button(
        text="Подробнее ⚡️",
        url="https://t.me/alnurs_test_bot?startapp",
    )
    keyboard_builder.adjust(2, 2, 1)

    return keyboard_builder.as_markup()


def get_action_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура действий админа

    :return: Клавиатура в сообщении
    """
    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.button(text="Новый опрос", callback_data="new")
    keyboard_builder.button(text="Старый опрос", callback_data="old")
    keyboard_builder.adjust(2)

    return keyboard_builder.as_markup()
