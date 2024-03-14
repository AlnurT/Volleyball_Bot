from datetime import datetime, timedelta

from aiogram.utils.formatting import Text, as_list

from src.database.orm import AsyncOrm


def my_numbered_list(*items):
    fmt = "      <code>{:<3}</code> "
    return as_list(
        *(Text(fmt.format(f"{index}."), item) for index, item in enumerate(items, 1))
    )


async def send_text(is_game=True):
    players_list = await AsyncOrm.get_players_list(True)
    day = datetime.now()

    if not is_game:
        return as_list(
            "🏁 <b>Игра завершена</b> 🏁\n",
            f"Вторник - {day.strftime('%d.%m')}\n",
            "👫 Участники:",
            my_numbered_list(*players_list),
            "\nВсем спасибо за игру!",
        )

    not_players_list = await AsyncOrm.get_players_list(False)
    day += timedelta(days=1)

    return as_list(
        f"🏐 <b>Игра во вторник - {day.strftime('%d.%m')}</b> 🏐\n",
        "👫 Участники:",
        my_numbered_list(*players_list),
        "\n🙅‍♂️ Не играют:",
        my_numbered_list(*not_players_list),
    )
