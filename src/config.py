from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        # postgresql+asyncpg://postgres:password@localhost:5432/sa
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
#     DB_HOST="localhost",
#     DB_PORT=5432,
#     DB_USER="postgres",
#     DB_PASS="password",
#     DB_NAME="postgres"
# )
