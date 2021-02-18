from contextlib import contextmanager
from typing import Optional, Union

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import Session, sessionmaker

from department_app.domain.interfaces import IDatabase

from .models import Base


class Database(IDatabase):
    def __init__(self, config):
        self._url: Union[str, URL] = config.DATABASE_URI

        self._engine: Optional[Engine] = None
        self._session: Optional[Session] = None

        self.testing = getattr(config, "TESTING", None)

    def connect(self) -> None:
        if self._url is None:
            raise ValueError("Database url is not configured.")
        self._engine = create_engine(self._url, echo=False)
        self._session = sessionmaker(bind=self._engine, expire_on_commit=False)()

        if self.testing:
            Base.metadata.create_all(self._engine)

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
