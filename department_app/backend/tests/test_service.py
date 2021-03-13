from datetime import date

from django.http import Http404
from django.test import TestCase

from ..models import Department, Employee
from ..service import delete, get_all, get_obj, save_obj, update


class TestService(TestCase):
    def setUp(self):
        Department.objects.create(id=555, name="Marketing department")
        Department.objects.create(id=666, name="Management department")
        Department.objects.create(id=777, name="Delete department")
        Employee.objects.create(
            id=555,
            fullname="Andrey Borsuk",
            salary=123.23,
            bday=date(1996, 6, 25),
            department=Department.objects.first(),
        )

    def test_get_all(self):
        self.assertEquals(len(get_all(Department)), 3)
        self.assertEquals(len(get_all(Employee)), 1)

    def test_get_all_returns_empty_list(self):
        self.assertEqual(get_all(Department, name__contains="no such department"), [])

    def test_get_obj(self):
        dep = get_obj(Department, id=555)
        self.assertEquals(dep.name, "Marketing department")
        emp = get_obj(Employee, id=555)
        self.assertEquals(emp.fullname, "Andrey Borsuk")

    def test_get_obj_raises_404(self):
        with self.assertRaises(Http404):
            get_obj(Department, id=1231231231231231)

    def test_update(self):
        update(Employee, id=555, new_fields={"salary": 200, "bday": date(2000, 5, 12)})
        emp = get_obj(Employee, id=555)
        self.assertEquals(int(emp.salary), 200)
        self.assertEquals(emp.bday, date(2000, 5, 12))

    def test_update_fails(self):
        with self.assertRaises(ValueError):
            update(12, id=123, new_fields={"name": 123})

        with self.assertRaises(TypeError):
            update(Employee, id=555, new_fields={"bday": 12})

    def test_save_obj(self):
        dep = Department(id=123, name="New department")
        save_obj(dep)
        self.assertEquals(len(get_all(Department)), 4)
        self.assertIn(dep, get_all(Department))

    def test_save_obj_fails(self):
        with self.assertRaises(ValueError):
            save_obj(Department(name="Marketing department"))

        with self.assertRaises(ValueError):
            save_obj(123)

    def test_delete_obj(self):
        delete(Department, id=777)
        self.assertEquals(len(get_all(Department)), 2)
        with self.assertRaises(Http404):
            get_obj(Department, id=777)

    def test_delete_obj_fails(self):
        with self.assertRaises(Http404):
            delete(Department, id=12312312312)

        with self.assertRaises(ValueError):
            delete(123, id=12321)
