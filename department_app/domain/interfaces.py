from abc import ABC, abstractmethod
from typing import ContextManager

from sqlalchemy.orm import Session  # type: ignore


class IDatabase(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def session(self) -> ContextManager[Session]:
        pass
