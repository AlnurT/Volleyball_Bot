from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.button(text="Буду играть 👍", callback_data="F")
    keyboard_builder.button(text="Не смогу 👎", callback_data="S")
    keyboard_builder.button(text="У меня +1 🤝", callback_data="T")
    keyboard_builder.button(text="У меня -1 🚷", callback_data="Th")
    keyboard_builder.adjust(2, 2)

    return keyboard_builder.as_markup()
