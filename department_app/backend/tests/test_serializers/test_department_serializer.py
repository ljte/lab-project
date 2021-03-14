from backend.models import Department
from backend.serializers import DepartmentSchema
from backend.service import get_obj, save_obj
from django.test import TestCase
from pydantic import ValidationError


class TestDepartmentSchema(TestCase):
    def setUp(self):
        save_obj(Department(id=555, name="Marketing department"))
        save_obj(Department(id=666, name="Management department"))

    def test_validation_passes(self):
        dep = DepartmentSchema.from_orm(get_obj(Department, id=555))
        self.assertEqual(dep.name, "Marketing department")
        dep = DepartmentSchema.parse_obj({"name": "Management"})
        self.assertEqual(dep.name, "Management department")

    def test_validation_fails(self):
        with self.assertRaises(ValidationError):
            DepartmentSchema.parse_obj({"name": "Marketing departmnet12312"})

    def test_dumps_creates_dict_from_orm_object(self):
        dep = DepartmentSchema.dumps(get_obj(Department, id=666))
        self.assertEqual(
            dep,
            {
                "id": 666,
                "name": "Management department",
                "number_of_employees": 0,
                "average_salary": 0,
            },
        )

    def test_dumps_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            DepartmentSchema.dumps(
                Department(id=12312, name="Finance 12312 department")
            )

    def test_loads_creates_orm_object_from_dict(self):
        dep = DepartmentSchema.loads({"id": 1000, "name": "Accounting department"})
        self.assertTrue(isinstance(dep, Department))
        self.assertEqual(dep.id, 1000)
        self.assertEqual(dep.name, "Accounting department")

    def test_loads_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            DepartmentSchema.loads({"id": 1000, "name": "Accounting12312 department"})
