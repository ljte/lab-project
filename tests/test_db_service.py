from datetime import datetime

import pytest

from department_app.database.models import Department, Employee
from department_app.domain.exceptions import InvalidModelError, ModelNotFoundError, RecordAlreadyExistsError, InvalidRecordError, RecordNotFoundError


def test_all(db_service):
    assert len(db_service.all(Department)) == 0


def test_all_with_invalid_model(db_service):
    with pytest.raises(ModelNotFoundError):
        db_service.all(123)


def test_insert(db_service):
    e = Employee(first_name="Andrey", second_name="Semenov", bday=datetime(1988, 12, 25), department_id=1)

    db_service.insert(e)
    assert len(db_service.all(Employee)) == 1
    assert db_service.get(Employee, first_name="Andrey").fullname == "Andrey Semenov"


def test_invalid_inserts(db_service):
    db_service.insert(Department(name="Management department"))
    with pytest.raises(RecordAlreadyExistsError):
        db_service.insert(Department(name="Management department"))


def test_get(db_service):
    db_service.insert(Department(name="Management department"))

    d = db_service.get(Department, name="Management department")
    assert d.name == "Management department"

    d = db_service.get(Department, name="123312")
    assert d is None


def test_get_invalid(db_service):
    with pytest.raises(InvalidModelError):
        db_service.get(12312, gasg='2312')
        db_service.get(Department, asgsa=12)


def test_update(db_service):
    db_service.insert(Department(name="Marketing department"))

    db_service.update(db_service.get(Department, name="Marketing department"), name="Management department")

    assert db_service.get(Department, name="Management department") is not None


def test_invalid_update(db_service):
    db_service.insert(Department(name="Marketing department"))

    with pytest.raises(InvalidRecordError):
        db_service.update(13123, name="Management department")
        db_service.update(db_service.get(Department, name="Marketing department"), asf=1231)


def test_delete(db_service):
    db_service.insert(Department(name="Marketing department"))

    assert len(db_service.all(Department)) == 1

    db_service.delete(db_service.get(Department, name="Marketing department"))

    assert len(db_service.all(Department)) == 0


def test_invalid_delete(db_service):
    with pytest.raises(RecordNotFoundError):
        db_service.delete(12312)
        db_service.delete(Department(name="Finance department"))