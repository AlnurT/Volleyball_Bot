from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import CallbackQuery, FSInputFile, Message

from src.base.bot import dp
from src.database.orm import AsyncOrm
from src.keyboards.inline import get_inline_keyboard
from src.utils.poll_message import send_text


@dp.message(Command("poll"))
async def get_poll(message: Message):
    await AsyncOrm.create_tables()
    text_for_poll = await send_text()
    await message.answer_photo(
        photo=FSInputFile("files/volleyball.jpg"),
        caption=text_for_poll.as_kwargs(parse_mode_key=ParseMode.HTML)["text"],
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
        await call.message.edit_caption(
            caption=text_for_poll.as_kwargs(parse_mode_key=ParseMode.HTML)["text"]
        )
        await call.message.edit_reply_markup(reply_markup=get_inline_keyboard())


def register_basic_handlers():
    pass
