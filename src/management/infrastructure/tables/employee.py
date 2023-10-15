from sqlalchemy import Column, DateTime, ForeignKey, String, Table, sql

from ..datasource import metadata

employee_table = Table(
    "employee",
    metadata,
    Column("id", String(40), primary_key=True),
    Column("first_name", String(150), nullable=False),
    Column("second_name", String(150), nullable=False),
    Column("email", String(200), nullable=False),
    Column(
        "hired_at",
        DateTime(timezone=True),
        server_default=sql.func.now(),
        nullable=False,
    ),
    Column(
        "department_id",
        String(40),
        ForeignKey("department.id"),
        nullable=False,
    ),
)
