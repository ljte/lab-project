import typing as t

from management.domain.model import Department, EntityId


class DepartmentMapper:
    @staticmethod
    def to_dict(department: Department) -> dict[str, t.Any]:
        return {
            "id": department.id(),
            "name": department.name,
            "created_at": department.created_at,
        }

    @staticmethod
    def from_dict(department: dict[str, t.Any]) -> Department:
        return Department(
            id=EntityId(department["id"]),
            name=department["name"],
            created_at=department["created_at"],
        )
