from aiogram.utils.formatting import as_list, as_numbered_list

from src.database.orm import AsyncOrm


async def send_text():
    players_list = await AsyncOrm.get_players_list()
    not_players_list = await AsyncOrm.get_not_players_list()

    return as_list(
        "Игра в четверг\n",
        "Участники:",
        as_numbered_list(*players_list, fmt="{}.    "),
        "",
        "Не играют:",
        as_numbered_list(*not_players_list, fmt="{}.    "),
    )
