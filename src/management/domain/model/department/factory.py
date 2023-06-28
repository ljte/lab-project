import typing as t
from datetime import datetime, timezone

from ..entity_id import EntityId
from .entity import Department


class DepartmentFactory:
    @staticmethod
    def make(name: str, id_: t.Optional[str] = None) -> Department:
        id_ = EntityId(id_)
        return Department(id=id_, name=name, created_at=datetime.now(timezone.utc))
