from abc import ABCMeta


def check_for_digits(s: str) -> bool:
    for c in s:
        if c.isdigit():
            return True
    return False


class Singleton(ABCMeta):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]