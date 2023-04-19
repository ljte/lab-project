import typing as t
from management.model import Employee, EntityId


class EmployeeMapper:
    @staticmethod
    def to_dict(employee: Employee) -> dict[str, t.Any]:
        return {
            "id": employee.id(),
            "first_name": employee.first_name,
            "second_name": employee.second_name,
            "email": employee.email,
            "department_id": employee.department_id,
            "hired_at": employee.hired_at,
        }

    @staticmethod
    def from_dict(employee: dict[str, t.Any]) -> Employee:
        return Employee(
            id=EntityId(employee['id']),
            first_name=employee['first_name'],
            second_name=employee['second_name'],
            email=employee['email'],
            department_id=employee['department_id'],
            hired_at=employee['hired_at'],
        )
