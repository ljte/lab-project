from abc import ABC, abstractmethod


class IDatabase(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def session(self):
        pass