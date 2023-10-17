from pydantic_settings import BaseSettings, SettingsConfigDict

from management.infrastructure.datasource import ConnectionParams


class DatabaseSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    database: str
    dialect: str
    driver: str

    model_config = SettingsConfigDict(env_prefix="DATABASE_")

    def to_connection_params(self) -> ConnectionParams:
        return ConnectionParams(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            dialect=self.dialect,
            driver=self.driver,
        )


class Settings(BaseSettings):
    database: DatabaseSettings
