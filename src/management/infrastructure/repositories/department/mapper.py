import typing as t

from management.model import Department, EntityId


class DepartmentMapper:
    def to_dict(department: Department) -> dict[str, t.Any]:
        return {
            "id": department.id(),
            "name": department.name,
            "created_at": department.created_at,
        }

    def from_dict(department: dict[str, t.Any]) -> Department:
        return Department(
            id=EntityId(department["id"]),
            name=department["name"],
            created_at=department["created_at"],
        )
