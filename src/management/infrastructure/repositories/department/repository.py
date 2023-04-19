from management.model import Department
from management.infrastructure.datasource import Database


class DepartmentRepository:
    def __init__(self, database: Database) -> None:
        self.db = database

    def save(self, department: Department) -> None:
        pass

    def find(self, department_id: str) -> Department:
        pass

    def delete(self, department_id: str) -> None:
        pass
