from pydantic import BaseSettings, Field


class PostgresSettings(BaseSettings):
    user: str
    password: str
    host: str
    port: str
    db: str

    class Config:
        env_prefix = "POSTGRES_"


class Settings(BaseSettings):
    database: PostgresSettings = PostgresSettings()
    secret_key: str
    debug: bool = False


settings = Settings()
