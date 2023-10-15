from sqlalchemy import Column, DateTime, String, Table, sql

from ..datasource import metadata

department_table = Table(
    "department",
    metadata,
    Column("id", String(40), primary_key=True),
    Column("name", String(200), nullable=False),
    Column(
        "created_at",
        DateTime(timezone=True),
        server_default=sql.func.now(),
        nullable=False,
    ),
)
