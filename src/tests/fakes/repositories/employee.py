import typing as t

from management.domain.model import Employee
from management.domain.interfaces import IEmployeeRepository


class FakeEmployeeRepository(IEmployeeRepository):
    def __init__(self, storage: t.Optional[dict[str, Employee]] = None) -> None:
        self._storage = storage or dict()

    def save(self, employee: Employee) -> None:
        self._storage[employee.id()] = employee

    def find(self, employee_id: str) -> Employee:
        employee = self._storage.get(employee_id)
        if employee is None:
            raise RuntimeError(f"Employee '{employee_id}' was not found")
        return employee

    def delete(self, employee_id: str) -> None:
        employee = self._storage.pop(employee_id)
        if employee is None:
            raise RuntimeError(f"Employee '{employee_id}' was not found")
