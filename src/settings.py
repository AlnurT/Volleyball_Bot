from dataclasses import dataclass

from environs import Env


@dataclass
class Bots:
    bot_token: str
    admin_id: int
    user: str
    password: str
    database: str
    host: str
    port: int


@dataclass
class Settings:
    bots: Bots


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str("BOT_TOKEN"),
            admin_id=env.int("ADMIN_ID"),
            user=env.str("USER"),
            password=env.str("PASSWORD"),
            database=env.str("DATABASE"),
            host=env.str("HOST"),
            port=env.int("PORT"),
        )
    )


settings = get_settings("config")
