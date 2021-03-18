from pydantic import BaseSettings, Field


class PostgresSettings(BaseSettings):
    user: str = "user"
    password: str = "user"
    host: str = "localhost"
    port: str = "5435"
    db: str = "user"

    class Config:
        env_prefix = "POSTGRES_"


class Settings(BaseSettings):
    database: PostgresSettings = PostgresSettings()
    secret_key: str = "DEBUG"
    debug: bool = False


settings = Settings()
