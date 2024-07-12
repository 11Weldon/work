from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings(
    DB_HOST="localhost",
    DB_PORT=5433,
    DB_USER="postgres",
    DB_PASS="mysecretpassword",
    DB_NAME="postgres"
)

# settings = Settings(
#     DB_HOST="db",
#     DB_PORT=5432,
#     DB_USER="postgres",
#     DB_PASS="mysecretpassword",
#     DB_NAME="postgres"
# )
