from contextlib import contextmanager
from typing import Optional, Union

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

from department_app.domain.helpers import Singleton
from department_app.domain.interfaces import IDatabase


class Database(IDatabase, metaclass=Singleton):
    def __init__(self, url: Optional[Union[str, URL]] = None):
        self._url = url

        self._engine: Optional[Engine] = None
        self._session: Optional[sessionmaker] = None

    def connect(self) -> None:
        if self._url is None:
            raise ValueError("Database url is not configured.")
        self._engine = create_engine(self._url, echo=False)
        self._session = sessionmaker(bind=self._engine, expire_on_commit=False)

    @contextmanager
    def session(self):
        if self._session is None:
            raise ValueError("Cannot create session. Connect to the database first.")
        session = self._session()
        yield session
        session.close()
