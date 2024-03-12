from datetime import datetime

from aiogram import Bot
from aiogram.enums import ParseMode

# from aiogram.filters import Command
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram.utils.formatting import as_list, as_numbered_list

from src.base.bot import bot, dp, scheduler
from src.config import settings
from src.database.orm import AsyncOrm
from src.keyboards.inline import get_inline_keyboard


async def send_text(is_game=True):
    players_list = await AsyncOrm.get_players_list(True)

    if not is_game:
        return as_list(
            "🏁 <b>Игра во вторник завершена</b> 🏁\n ",
            "👫 Участники:",
            as_numbered_list(*players_list, fmt="      {}.    "),
            " ",
        )

    not_players_list = await AsyncOrm.get_players_list(False)

    return as_list(
        "🏐 <b>Игра во вторник</b> 🏐\n",
        "👫 Участники:",
        as_numbered_list(*players_list, fmt="      {}.    "),
        "\n🙅‍♂️ Не играют:",
        as_numbered_list(*not_players_list, fmt="      {}.    "),
    )


async def get_poll_cron(chat_bot: Bot):
    await AsyncOrm.create_tables()
    message = await chat_bot.send_photo(
        chat_id=settings.BOT_CHAT_ID,
        photo=FSInputFile("files/volleyball.jpg"),
        caption="🏐 <b>Игра во вторник</b> 🏐\n",
        reply_markup=get_inline_keyboard(),
    )
    scheduler.add_job(
        end_poll,
        trigger="cron",
        hour=datetime.now().hour,
        minute=datetime.now().minute + 1,
        start_date=datetime.now(),
        kwargs={"message": message},
    )


async def end_poll(message: Message):
    text_for_poll = await send_text(False)
    await message.answer_photo(
        photo=FSInputFile("files/volleyball.jpg"),
        caption=text_for_poll.as_kwargs(parse_mode_key=ParseMode.HTML)["text"],
    )


@dp.callback_query()
async def play_game(call: CallbackQuery):
    user_id = call.from_user.id
    name = call.from_user.first_name

    if call.data in ("is_play_true", "is_play_false"):
        is_game = True if call.data == "is_play_true" else False
        is_change = await AsyncOrm.update_pl_status(user_id, name, is_game)
    else:
        extra_pl = 1 if call.data == "plus_extra_pl" else -1
        is_change = await AsyncOrm.update_extra_pl(user_id, name, extra_pl=extra_pl)

    if is_change:
        text_for_poll = await send_text()
        await call.message.edit_caption(
            caption=text_for_poll.as_kwargs(parse_mode_key=ParseMode.HTML)["text"]
        )
        await call.message.edit_reply_markup(reply_markup=get_inline_keyboard())


def register_basic_handlers():
    scheduler.add_job(
        get_poll_cron,
        trigger="cron",
        hour=datetime.now().hour,
        minute=datetime.now().minute,
        second=datetime.now().second + 5,
        start_date=datetime.now(),
        kwargs={"chat_bot": bot},
    )
