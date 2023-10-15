import typing as t
from uuid import uuid4

from management.domain.exceptions import DepartmentNotFoundError
from management.domain.interfaces import IDepartmentRepository
from management.domain.model import Department, DepartmentFactory


def generate_department(
    name: t.Optional[str] = None, id_: t.Optional[str] = None
) -> Department:
    name = name or str(uuid4())
    return DepartmentFactory.make(id_=id_, name=name)


class FakeDepartmentRepository(IDepartmentRepository):
    def __init__(
        self, storage: t.Optional[dict[str, Department]] = None
    ) -> None:
        self._storage = storage or dict()

    def save(self, department: Department) -> None:
        self._storage[department.id()] = department

    def find(self, department_id: str) -> Department:
        department = self._storage.get(department_id)
        if department is None:
            raise DepartmentNotFoundError(department_id)
        return department

    def delete(self, department_id: str) -> None:
        department = self._storage.pop(department_id)
        if department is None:
            raise DepartmentNotFoundError(department_id)
