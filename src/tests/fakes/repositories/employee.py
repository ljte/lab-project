import typing as t
from uuid import uuid4

from management.domain.exceptions import EmployeeNotFoundError
from management.domain.interfaces import IEmployeeRepository
from management.domain.model import Employee, EmployeeFactory


def generate_employee(
    first_name: t.Optional[str] = None,
    second_name: t.Optional[str] = None,
    email: t.Optional[str] = None,
    department_id: t.Optional[str] = None,
    id_: t.Optional[str] = None,
) -> Employee:
    first_name = first_name or str(uuid4())
    second_name = second_name or str(uuid4())
    return EmployeeFactory.make(
        first_name=first_name,
        second_name=second_name,
        email=email or f"{first_name}_{second_name}@gmail.com",
        department_id=department_id or str(uuid4()),
        id_=id_ or str(uuid4()),
    )


class FakeEmployeeRepository(IEmployeeRepository):
    def __init__(self, storage: t.Optional[dict[str, Employee]] = None) -> None:
        self._storage = storage or dict()

    def save(self, employee: Employee) -> None:
        self._storage[employee.id()] = employee

    def find(self, employee_id: str) -> Employee:
        employee = self._storage.get(employee_id)
        if employee is None:
            raise EmployeeNotFoundError(employee_id)
        return employee

    def delete(self, employee_id: str) -> None:
        employee = self._storage.pop(employee_id)
        if employee is None:
            raise EmployeeNotFoundError(employee_id)

    def all_employees_of_department(self, department_id: str) -> list[Employee]:
        return [
            employee
            for employee in self._storage.values()
            if employee.department_id == department_id
        ]
