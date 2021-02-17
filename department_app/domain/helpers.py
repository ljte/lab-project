from flask import g


def check_for_digits(s: str) -> bool:
    for c in s:
        if c.isdigit():
            return True
    return False


def get_service():
    if "service" not in g:
        raise ValueError("Database service wasn't configured properly")
    return g.service


def get_db():
    if "database" not in g:
        raise ValueError("Database wasn't configured properly")
    return g.database


# class Singleton(ABCMeta):

#     _instances: Dict[Type, Type] = {}

#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]
