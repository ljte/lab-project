import pytest

from department_app.config import TestConfig
from department_app.database import Database, Base
from department_app.service import DatabaseService
from department_app import create_app


@pytest.fixture()
def db_service():
    db = Database(TestConfig())
    db.connect()
    return DatabaseService(db)


@pytest.fixture
def client():
    app = create_app(TestConfig())
    with app.app_context():
        yield app.test_client()
