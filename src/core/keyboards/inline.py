from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.button(text="Буду играть 👍", callback_data="is_play_true")
    keyboard_builder.button(text="Не смогу 👎", callback_data="is_play_false")
    keyboard_builder.button(text="У меня +1 🤝", callback_data="plus_extra_pl")
    keyboard_builder.button(text="У меня -1 🚷", callback_data="minus_extra_pl")
    keyboard_builder.adjust(2, 2)

    return keyboard_builder.as_markup()
