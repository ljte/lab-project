import typing as t
from uuid import uuid4


class EntityId:
    def __init__(self, id_: t.Optional[str] = None) -> None:
        self.value = id or str(uuid4())

    def __call__(self) -> str:
        return self.value

    def __eq__(self, other: "EntityId") -> bool:
        return isinstance(other, type(self)) and self.value == other.value

    def repr(self) -> str:
        return f"EntityId({self.value=})"
