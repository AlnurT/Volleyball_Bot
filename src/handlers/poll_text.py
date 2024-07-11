from datetime import datetime

from aiogram.utils.formatting import Text, as_list

from src.database.orm import VlPlayersOrm


def my_numbered_list(*items) -> Text:
    """
    Функция для тонкой настройки вывода игроков

    :param items: Список игроков
    :return: Форматированный список игроков
    """
    fmt = "      <code>{:<3}</code> "
    return as_list(
        *(Text(fmt.format(f"{index}."), item) for index, item in enumerate(items, 1))
    )


async def send_poll() -> Text:
    """
    Вывод текстовой части опроса при голосовании

    :return: Текст опроса по строкам
    """
    players_list = await VlPlayersOrm.get_players_list(True)
    not_players_list = await VlPlayersOrm.get_players_list(False)
    reserve = ""

    if len(players_list) > 14:
        reserve = as_list("\n⏳ Резерв:", my_numbered_list(*players_list[14:]), "")
        players_list = players_list[:14]

    return as_list(
        "🏐 <b>Игра во вторник</b> 🏐\n",
        "👫 Участники:",
        my_numbered_list(*players_list),
        reserve,
        "🙅‍♂️ Не играют:",
        my_numbered_list(*not_players_list),
    )


async def send_end_of_poll() -> Text:
    """
    Вывод текстовой части опроса после голосования

    :return: Текст опроса по строкам
    """
    players_list = await VlPlayersOrm.get_players_list(True)
    day = datetime.now().strftime("%d.%m")

    return as_list(
        "🏁 <b>Игра завершена</b> 🏁\n",
        f"Вторник - {day}\n",
        "👫 Участники:",
        my_numbered_list(*players_list),
        "\nВсем спасибо за игру!",
    )
