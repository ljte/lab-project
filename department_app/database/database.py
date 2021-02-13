from typing import Optional, Union
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker


class Database:

    def __init__(self, url: Union[str, URL]):
        self._url = url

        self._engine: Optional[Engine] = None
        self._session: Optional[sessionmaker] = None

    def connect(self) -> None:
        self._engine = create_engine(self._url, echo=False)
        self._session = sessionmaker(bind=self._engine)
    
    @contextmanager
    def session(self):
        session = self._session()
        yield session
        session.close()