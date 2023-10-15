from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    db: str
    dialect: str
    driver: str

    model_config = SettingsConfigDict(env_prefix="DATABASE_")


class Settings(BaseSettings):
    database: DatabaseSettings = DatabaseSettings()
