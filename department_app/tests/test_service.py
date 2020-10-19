"""test database services"""

import unittest
from datetime import date

from werkzeug.exceptions import BadRequest, NotFound

from department_app import service, db, app
from department_app.models import Department, Employee
from department_app.config import TestConfig


class TestService(unittest.TestCase):
    """class for testing database services (crud operations)"""
    @classmethod
    def setUpClass(cls):
        """setup db"""
        app.config.from_object(TestConfig)
        db.create_all()
        service.insert_into_db(Department(id=2, name='Marketing department'))
        service.insert_into_db(Employee(id=2, fullname='Sergey Nemko',
                                        bday=date(1998, 12, 25), salary=555, department_id=2))

    def test_get_all(self):
        """test getting all the department and employees"""

        self.assertListEqual(service.get_all(Department), Department.query.all())
        self.assertListEqual(service.get_all(Employee), Employee.query.all())

        with self.assertRaises(ValueError):
            service.get_all('gasgas')
            service.get_all(412412)

    def test_get_or_404(self):
        """test getting a single department or an employee"""

        self.assertEqual(service.get_or_404(Department, id=2), Department.query.filter_by(id=2).first())
        self.assertEqual(service.get_or_404(Department, name='Marketing department'),
                         Department.query.filter_by(name='Marketing department').first())

        self.assertEqual(service.get_or_404(Employee, id=2), Employee.query.filter_by(id=2).first())
        self.assertEqual(service.get_or_404(Employee, department_id=2),
                         Employee.query.filter_by(department_id=2).first())

        with self.assertRaises(NotFound):
            service.get_or_404(Department, id='gsdas')
            service.get_or_404(12312, id=1)

    def test_delete_from_db(self):
        """test deleting a department or an employee"""

        service.insert_into_db(Department(id=100, name='Delete department'))
        service.insert_into_db(Employee(id=100, fullname='Delete Employee',
                                        bday=date(1998, 12, 24), salary=231, department_id=1))

        dep = service.get_or_404(Department, name='Delete department')
        emp = service.get_or_404(Employee, fullname='Delete Employee')

        service.delete_from_db(dep)
        service.delete_from_db(emp)

        self.assertNotIn(dep, Department.query.all())
        self.assertNotIn(emp, Employee.query.all())

        with self.assertRaises(BadRequest):
            service.delete_from_db('gas')
            service.delete_from_db(124)

    def test_insert_into_db(self):
        """test adding a new department or an employee"""

        dep = Department(id=150, name='Insert department')
        emp = Employee(id=150, fullname='Insert Employee',
                       bday=date(1994, 10, 23), salary=321, department_id=1)

        service.insert_into_db(dep)
        service.insert_into_db(emp)

        self.assertIn(dep, Department.query.all())
        self.assertIn(emp, Employee.query.all())

        with self.assertRaises(BadRequest):
            service.insert_into_db('gsd')
            service.insert_into_db(412)

        service.delete_from_db(dep)
        service.delete_from_db(emp)

    def test_update_department(self):
        """test updating a department"""

        dep = Department(id=200, name='Update department')
        service.insert_into_db(dep)

        service.update_record(Department, dep, name='Super department')

        self.assertEqual(dep.name, 'Super department')

        service.delete_from_db(dep)

        with self.assertRaises(BadRequest):
            service.update_record('gas', dep, name='My department')
            service.update_record(Department, 12, name='My department')
            service.update_record(Department, dep)

    def test_update_employee(self):
        """test updating an employee"""

        emp = Employee(id=200, fullname='Update Employee',
                       bday=date(1998, 11, 14), salary=312, department_id=1)
        service.insert_into_db(emp)

        service.update_record(Employee, emp, fullname='Super Employee', bday=date(2000, 2, 20), salary=500)

        self.assertEqual(emp.fullname, 'Super Employee')
        self.assertEqual(emp.bday, date(2000, 2, 20))
        self.assertEqual(int(emp.salary), 500)

        with self.assertRaises(BadRequest):
            service.update_record('gas', emp, name='My Employee')
            service.update_record(Department, 12, name='My Employee')
            service.update_record(Department, emp)

        service.delete_from_db(emp)


if __name__ == "__main__":
    unittest.main()
