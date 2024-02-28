from aiogram.utils.formatting import as_list, as_numbered_list

from src.database.orm import AsyncOrm


async def send_text():
    players_list = await AsyncOrm.get_players_list(True)
    not_players_list = await AsyncOrm.get_players_list(False)
    players_num = 0 if players_list[0] == "" else len(players_list)

    if players_num == 1:
        word = "игрок"
    elif 1 < players_num < 5:
        word = "игрока"
    else:
        word = "игроков"

    return as_list(
        "<b>Игра в четверг</b>\n",
        "Участники:",
        as_numbered_list(*players_list, fmt="{}.    "),
        f"\n{len(players_list)} {word}\n",
        "Не играют:",
        as_numbered_list(*not_players_list, fmt="{}.    "),
    )
