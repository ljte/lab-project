from management.domain.model import Employee
from management.infrastructure.datasource import Database
from management.domain.interfaces import IEmployeeRepository


class EmployeeRepository(IEmployeeRepository):
    def __init__(self, database: Database) -> None:
        self.db = database

    def save(self, employee: Employee) -> None:
        pass

    def find(self, employee_id: str) -> Employee:
        pass

    def all_of_department(self, department_id: str) -> list[Employee]:
        pass

    def delete(self, employee_id: str) -> None:
        pass
