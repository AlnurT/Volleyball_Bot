from environs import Env


class Settings:
    BOT_TOKEN: str
    BOT_ADMIN_ID: int
    BOT_CHAT_ID: int
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def database_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    def get_settings(self, path: str):
        env = Env()
        env.read_env(path)

        self.BOT_TOKEN = env.str("BOT_TOKEN")
        self.BOT_ADMIN_ID = env.int("ADMIN_ID")
        self.BOT_CHAT_ID = env.int("CHAT_ID")
        self.DB_USER = env.str("DB_USER")
        self.DB_PASS = env.str("DB_PASS")
        self.DB_NAME = env.str("DB_NAME")
        self.DB_HOST = env.str("DB_HOST")
        self.DB_PORT = env.int("DB_PORT")


settings = Settings()
settings.get_settings(".env")
