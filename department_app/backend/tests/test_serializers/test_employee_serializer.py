from datetime import date

from django.test import TestCase
from pydantic import ValidationError

from backend.models import Department, Employee
from backend.serializers import EmployeeSchema
from backend.service import get_obj, save_obj


class TestDepartmentSchema(TestCase):
    def setUp(self):
        save_obj(Department(id=666, name="Management department"))
        save_obj(
            Employee(
                id=555,
                fullname="First Employee",
                bday=date(1998, 12, 25),
                salary=123.32,
                department=get_obj(Department, id=666),
            )
        )
        save_obj(
            Employee(
                id=666,
                fullname="Second Employee",
                bday=date(1995, 9, 12),
                salary=534.2,
                department=get_obj(Department, id=666),
            )
        )

    def test_validation_passes(self):
        emp = EmployeeSchema.from_orm(get_obj(Employee, id=555))
        self.assertEqual(emp.fullname, "First Employee")
        self.assertEqual(int(emp.salary), 123)
        self.assertEqual(emp.bday, date(1998, 12, 25))

    def test_validation_fails(self):
        with self.assertRaises(ValidationError):
            EmployeeSchema.parse_obj({"fullname": "First12312 Employee"})

    def test_dumps_creates_dict_from_orm_object(self):
        emp = EmployeeSchema.dumps(get_obj(Employee, id=666))
        self.assertEqual(
            emp,
            {
                "id": 666,
                "fullname": "Second Employee",
                "bday": date(1995, 9, 12),
                "salary": 534.2,
                "department": "Management department",
            },
        )

    def test_dumps_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            EmployeeSchema.dumps(
                Employee(
                    id=12312,
                    fullname="Third12312 Employee",
                    bday=date(1994, 10, 24),
                    salary=12331.123,
                    department=get_obj(Department, id=666),
                )
            )

    def test_loads_creates_orm_object_from_dict(self):
        emp = EmployeeSchema.loads(
            {
                "id": 1000,
                "fullname": "Fourth Employee",
                "bday": date(1992, 10, 24),
                "salary": 434.23,
                "department": "Management department",
            }
        )
        self.assertTrue(isinstance(emp, Employee))
        self.assertEqual(emp.id, 1000)
        self.assertEqual(emp.fullname, "Fourth Employee")
        self.assertEqual(emp.department, get_obj(Department, id=666))

    def test_loads_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            EmployeeSchema.loads(
                {
                    "id": 1000,
                    "fullname": "Test12312 Employee",
                    "salary": 12312.32,
                    "bday": 123,
                    "department": 1231,
                }
            )
