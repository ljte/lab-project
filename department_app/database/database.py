from contextlib import contextmanager
from typing import Optional, Union

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import Session, sessionmaker

from department_app.domain.interfaces import IDatabase


class Database(IDatabase):
    def __init__(self, url: Optional[Union[str, URL]] = None):
        self._url = url

        self._engine: Optional[Engine] = None
        self._session: Optional[Session] = None

    def connect(self) -> None:
        if self._url is None:
            raise ValueError("Database url is not configured.")
        self._engine = create_engine(self._url, echo=False)
        self._session = sessionmaker(bind=self._engine, expire_on_commit=False)()

    @contextmanager
    def session(self):
        if self._session is None:
            raise ValueError("Cannot create session. Connect to the database first.")
        try:
            yield self._session
        except Exception:
            self._session.rollback()
            raise        
        finally:
            self._session.close()
        
