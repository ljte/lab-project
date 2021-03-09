from datetime import date

from django.http import Http404
from django.test import TestCase

from ..models import Department, Employee
from ..service import delete, save_obj, update


class TestSevice(TestCase):
    def setUp(self):
        d = Department.objects.create(name="Marketing department")
        Department.objects.create(name="Management department")
        Employee.objects.create(
            first_name="Andrey",
            second_name="Semenov",
            salary=341.2,
            bday=date(1995, 12, 10),
            department=d,
        )

    def test_save_obj_with_proper_params(self):
        d = Department(name="Finance department")
        save_obj(d)
        self.assertIn(d, Department.objects.all())
        e = Employee(
            first_name="Semen",
            second_name="Borunov",
            salary=3523.2,
            bday=date(1999, 12, 19),
            department=Department.objects.first(),
        )
        save_obj(e)
        self.assertIn(e, Employee.objects.all())

    def test_save_obj_with_wrong_params(self):
        with self.assertRaises(ValueError):
            save_obj(1231)
            save_obj(Department(name="Management department"))

    def test_update_works_correctly(self):
        d = Department.objects.first()
        update(Department, id=d.id, name="Accounting department")
        self.assertEqual(Department.objects.get(id=d.id).name, "Accounting department")

    def test_update_raises_exceptions(self):
        with self.assertRaises(ValueError):
            update(123, id=1, name="asgas")

        with self.assertRaises(Http404):
            update(Department, id=1142412412, name="sdgsd")

    def test_delete_actually_deletes(self):
        emp = Employee.objects.first()
        delete(Employee, id=emp.id)
        self.assertNotIn(emp, Employee.objects.all())

    def test_delete_raises_exceptions(self):
        with self.assertRaises(ValueError):
            delete(123, id=1)
