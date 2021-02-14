from typing import ContextManager
from abc import ABC, abstractmethod

from sqlalchemy.orm import Session


class IDatabase(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def session(self) -> ContextManager[Session]:
        pass