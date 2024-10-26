import os


async def clear_log() -> None:
    """Очистка лог файла"""

    async with open(os.path.abspath("logs/bot.log"), "w") as _:
        pass
