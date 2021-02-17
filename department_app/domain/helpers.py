from abc import ABCMeta
from typing import Dict, Type

from flask import g

from .interfaces import IDatabase


def check_for_digits(s: str) -> bool:
    for c in s:
        if c.isdigit():
            return True
    return False


class Singleton(ABCMeta):

    _instances: Dict[Type, Type] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
