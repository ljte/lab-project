import typing as t
from uuid import uuid4


class EntityId:
    def __init__(self, id_: t.Optional[str] = None) -> None:
        self.id = id or str(uuid4())

    def __call__(self) -> str:
        return self.id
