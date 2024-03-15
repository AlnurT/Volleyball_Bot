from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_poll_keyboard():
    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.button(text="Буду играть 👍", callback_data="is_play_true")
    keyboard_builder.button(text="Не смогу 👎", callback_data="is_play_false")
    keyboard_builder.button(text="У меня +1 🤝", callback_data="plus_extra_pl")
    keyboard_builder.button(text="У меня -1 🚷", callback_data="minus_extra_pl")
    keyboard_builder.adjust(2, 2)

    return keyboard_builder.as_markup()


def get_keyboard_tables():
    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.button(text="Новый опрос", callback_data="new_poll")
    keyboard_builder.button(text="Старый опрос", callback_data="old_poll")
    keyboard_builder.button(text="Закрыть опрос", callback_data="end_poll")
    keyboard_builder.adjust(2, 1)

    return keyboard_builder.as_markup()
