from contextlib import AbstractContextManager, contextmanager
from dataclasses import dataclass
from typing import Self, Union

from sqlalchemy import Connection, MetaData, create_engine, URL

__all__ = ["metadata", "ConnectionParams", "Database"]

metadata = MetaData()


@dataclass(frozen=True)
class ConnectionParams:
    host: str
    port: int
    user: str
    password: str
    dialect: str
    database: str
    driver: str

    @property
    def drivername(self) -> str:
        return f"{self.dialect}+{self.driver}"


class Database:
    def __init__(self, url: Union[str, URL]) -> None:
        self._engine = create_engine(url)

    @classmethod
    def sqlite(cls, filename: str) -> Self:
        return cls(f"sqlite:///{filename}")

    @classmethod
    def serverdb(cls, params: ConnectionParams) -> Self:
        return cls(
            URL.create(
                drivername=params.drivername,
                host=params.host,
                port=params.port,
                username=params.user,
                password=params.password,
                database=params.database,
            )
        )

    @contextmanager
    def conn(self) -> AbstractContextManager[Connection]:
        connection = self._engine.connect()
        try:
            yield connection
        except Exception:
            connection.rollback()
            raise
        else:
            connection.commit()
        finally:
            connection.close()
