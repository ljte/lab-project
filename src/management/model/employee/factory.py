import typing as t
from datetime import datetime, timezone

from ..entity_id import EntityId
from .entity import Employee


class EmployeeFactory:
    @staticmethod
    def make(
        first_name: str,
        second_name: str,
        email: str,
        department_id: str,
        id_: t.Optional[str] = None,
    ) -> Employee:
        pass
        id_ = EntityId(id_)
        return Employee(
            id=id_,
            first_name=first_name,
            second_name=second_name,
            email=email,
            department_id=department_id,
            hired_at=datetime.now(timezone.utc),
        )
