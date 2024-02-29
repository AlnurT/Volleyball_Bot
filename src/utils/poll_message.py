from aiogram.utils.formatting import as_list, as_numbered_list

from src.database.orm import AsyncOrm


async def send_text():
    players_list = await AsyncOrm.get_players_list(True)
    not_players_list = await AsyncOrm.get_players_list(False)

    return as_list(
        "🏐 <b>Игра в четверг</b>\n",
        "👫 Участники:",
        as_numbered_list(*players_list, fmt="      {}.    "),
        "\n🙅‍♂️ Не играют:",
        as_numbered_list(*not_players_list, fmt="      {}.    "),
    )
