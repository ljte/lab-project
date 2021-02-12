from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.url import URL


class DataBase:

    def __init__(
        self, user: str, password: str, host: str, port: str, database: str
    ):
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._database = database

        self._url: Optional[URL] = None
        self._engine: Optional[Engine] = None

    def connect(self) -> None:
        self._url = URL(
            "postgres+psycopg2",
            username=self._user,
            password=self._password,
            host=self._host,
            port=self._port,
            database=self._database
        )
        self._engine = create_engine(self._url, echo=False)