from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChatMember

from settings import CHAT_ID, ADMIN_ID


async def set_main_menu(bot: Bot):
    """ Список с командами и их описанием для кнопки menu """

    commands = [
        BotCommand(command="action", description="Выбор действия"),
    ]

    await bot.set_my_commands(
        commands,
        BotCommandScopeChatMember(chat_id=CHAT_ID, user_id=ADMIN_ID)
    )
