from sqlalchemy import select, Select, Column, delete, Delete, insert, Insert, bindparam

from management.domain.model import Department
from management.infrastructure.datasource import Database
from management.infrastructure.tables import department_table
from .mapper import DepartmentMapper


class QueryBuilder:
    @property
    def department_table_columns() -> tuple[Column]:
        return (
            department_table.c.id,
            department_table.c.name,
            department_table.c.created_at,
        )

    @classmethod
    def select_department_with_id(cls, department_id: str) -> Select:
        return select(cls.department_table_columns).where(
            department_table.c.id == department_id
        )

    @staticmethod
    def delete_department_with_id(department_id: str) -> Delete:
        return delete(department_table).where(
            department_table.c.id == department_id
        )

    @staticmethod
    def insert_department() -> Insert:
        return insert(department_table).values(
            id=bindparam("id"),
            name=bindparam("name"),
            created_at=bindparam("created_at")
        )

from management.domain.interfaces import IDepartmentRepository


class DepartmentRepository(IDepartmentRepository):
    def __init__(self, database: Database) -> None:
        self.db = database
        self.query_builder = QueryBuilder

    def save(self, department: Department) -> None:
        query = self.query_builder.insert_department()

        with self.db.conn() as conn:
            conn.execute(query, DepartmentMapper.to_dict(department))

    def find(self, department_id: str) -> Department:
        query = self.query_builder.select_department_with_id(department_id)
        with self.db.conn() as conn:
            department = conn.execute(query).fetchone()
            if department is None:
                raise RuntimeError(f"Not found {department_id}")
            return DepartmentMapper.from_dict(department)

    def delete(self, department_id: str) -> None:
        query = self.query_builder.delete_department_with_id(department_id)

        with self.db.conn() as conn:
            if conn.execute(query).rowcount == 0:
                raise RuntimeError(f"Not found {department_id}")
