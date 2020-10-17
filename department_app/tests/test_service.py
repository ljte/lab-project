import unittest
from datetime import date

from werkzeug.exceptions import BadRequest, NotFound

from department_app import service
from department_app.models import Department, Employee


service.reload_db()


class TestService(unittest.TestCase):

    def test_get_or_404(self):
        dep = service.get_or_404(Department, 1)
        emp = service.get_or_404(Employee, 1)

        self.assertEqual(dep, Department.query.filter_by(id=1).first())
        self.assertEqual(emp, Employee.query.filter_by(id=1).first())

        with self.assertRaises(BadRequest):
            service.get_or_404(Department, 'fgasgas')

        with self.assertRaises(NotFound):
            service.get_or_404(Employee, -5335)

    def test_get_all(self):
        all_deps = service.get_all(Department)
        all_emps = service.get_all(Employee)

        self.assertListEqual(all_deps, Department.query.all())
        self.assertListEqual(all_emps, Employee.query.all())

    def test_insert(self):
        dep = Department(name="Accounting department")
        emp = Employee(fullname="Semen Borunov",
                       bday=date(1998, 4, 18),
                       salary=424.32,
                       department_id=1)

        service.insert_into_db(Department, dep)
        service.insert_into_db(Employee, emp)

        self.assertIn(dep, Department.query.all())
        self.assertIn(emp, Employee.query.all())

    def test_delete(self):
        dep = Department.query.all()[-1]
        emp = Employee.query.all()[-1]

        service.delete_from_db(Department, dep)
        service.delete_from_db(Employee, emp)

        self.assertNotIn(dep, Department.query.all())
        self.assertNotIn(emp, Employee.query.all())

    def test_validate_department_name(self):
        self.assertFalse(Department.validate_name(''))
        self.assertFalse(Department.validate_name('   '))
        self.assertFalse(Department.validate_name('412412'))
        self.assertFalse(Department.validate_name('Managementdepartment'))

        self.assertTrue(Department.validate_name('Testing department'))

    def test_update_department_name(self):
        dep = service.get_or_404(Department, 1)
        service.update_department_name(dep, 'New department')

        self.assertEqual(service.get_or_404(Department, 1).name, 'New department')

        with self.assertRaises(BadRequest):
            service.update_department_name(dep, '421')

    def test_validate_employee_fullname(self):
        self.assertFalse(Employee.validate_fullname('412412'))
        self.assertFalse(Employee.validate_fullname('  '))
        self.assertFalse(Employee.validate_fullname(''))
        self.assertFalse(Employee.validate_fullname('gsdgds'))
        self.assertFalse(Employee.validate_fullname('42323 312'))
        self.assertFalse(Employee.validate_fullname('gsdgds 423'))

        self.assertTrue(Employee.validate_fullname('some name'))
        self.assertTrue(Employee.validate_fullname('Semen Borodko'))

    def test_update_employee(self):
        emp = service.get_or_404(Employee, 1)
        service.update_employee(emp, {'fullname': 'Andrey Semenov',
                                      'bday': date(1995, 12, 10),
                                      'salary': 412,
                                      'dep_name': 'Marketing department'})

        updated = service.get_or_404(Employee, 1)
        self.assertEqual(updated.fullname, 'Andrey Semenov')
        self.assertEqual(updated.bday, date(1995, 12, 10))
        self.assertEqual(updated.salary, 412)
        self.assertEqual(updated.department.name, 'Marketing department')

        with self.assertRaises(BadRequest):
            service.update_employee(emp, {'fullname': 'gasd 412'})
            service.update_employee(emp, {'salary': 'gsd'})
            service.update_employee(emp, {'dep_name': 'gssgdgsagwasrg'})

        with self.assertRaises(ValueError):
            service.update_employee(emp, {'bday': date(1999, 12, 32)})


if __name__ == "__main__":
    unittest.main()
