import pytest

from department_app.config import TestConfig
from department_app.database import Database, Base
from department_app.service import DatabaseService


@pytest.fixture()
def db_service():
    db = Database(TestConfig().DATABASE_URI)
    db.connect()
    Base.metadata.create_all(db._engine)
    return DatabaseService(db)
