import typing as t

from management.domain.interfaces import IDepartmentRepository
from management.domain.model import Department


class FakeDeparmentRepository(IDepartmentRepository):
    def __init__(
        self, storage: t.Optional[dict[str, Department]] = None
    ) -> None:
        self._storage = storage or dict()

    def save(self, department: Department) -> None:
        self._storage[department.id()] = department

    def find(self, department_id: str) -> Department:
        department = self._storage.get(department_id)
        if department is None:
            raise RuntimeError(f"Deparment '{department_id}' was not found")
        return department

    def delete(self, department_id: str) -> None:
        department = self._storage.pop(department_id)
        if department is None:
            raise RuntimeError(f"Deparment '{department_id}' was not found")
