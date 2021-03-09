from pydantic import BaseSettings, Field


class PostgresSettings(BaseSettings):
    user: str = Field(..., env="POSTGRES_USER")
    password: str = Field(..., env="POSTGRES_PASSWORD")
    host: str = Field(..., env="POSTGRES_HOST")
    port: str = Field(..., env="POSTGRES_PORT")
    db: str = Field(..., env="POSTGRES_DB")


class Settings(BaseSettings):
    database: PostgresSettings = PostgresSettings()
    secret_key: str = Field(...)
    debug: bool = Field(None)


settings = Settings()
