"""test database services"""

import unittest
from datetime import date

from werkzeug.exceptions import BadRequest, NotFound, InternalServerError

from department_app.service import utils
from department_app.models import db
from department_app.models.department import Department
from department_app.models.employee import Employee
from department_app import create_app
from department_app.config import TestConfig


class TetsService(unittest.TestCase):
    """class for testing database utilss (crud operations)"""
    @classmethod
    def setUpClass(cls):
        """setup db"""
        cls.app = create_app(app_config=TestConfig)
        cls.context = cls.app.app_context
        with cls.context():
            db.create_all()
            utils.insert_into_db(Department(id=2, name='Marketing department'))
            utils.insert_into_db(Employee(id=2, fullname='Sergey Nemko',
                                          bday=date(1998, 12, 25), salary=555, department_id=2))

    def test_get_all(self):
        """test getting all the department and employees"""
        with self.context():
            self.assertListEqual(utils.get_all(Department), Department.query.all())
            self.assertListEqual(utils.get_all(Employee), Employee.query.all())

            with self.assertRaises(ValueError):
                utils.get_all('gasgas')
                utils.get_all(412412)

    def test_get_or_404(self):
        """test getting a single department or an employee"""
        with self.context():
            self.assertEqual(utils.get_or_404(Department, id=2), Department.query.filter_by(id=2).first())
            self.assertEqual(utils.get_or_404(Department, name='Marketing department'),
                             Department.query.filter_by(name='Marketing department').first())

            self.assertEqual(utils.get_or_404(Employee, id=2), Employee.query.filter_by(id=2).first())
            self.assertEqual(utils.get_or_404(Employee, department_id=2),
                             Employee.query.filter_by(department_id=2).first())

            with self.assertRaises(NotFound):
                utils.get_or_404(Department, id='gsdas')
                utils.get_or_404(12312, id=1)

    def test_delete_from_db(self):
        """test deleting a department or an employee"""
        with self.context():
            utils.insert_into_db(Department(id=100, name='Delete department'))
            utils.insert_into_db(Employee(id=100, fullname='Delete Employee',
                                          bday=date(1998, 12, 24), salary=231, department_id=1))

            dep = utils.get_or_404(Department, name='Delete department')
            emp = utils.get_or_404(Employee, fullname='Delete Employee')

            utils.delete_from_db(dep)
            utils.delete_from_db(emp)

            self.assertNotIn(dep, Department.query.all())
            self.assertNotIn(emp, Employee.query.all())

            with self.assertRaises(BadRequest):
                utils.delete_from_db('gas')
                utils.delete_from_db(124)

            with self.assertRaises(InternalServerError):
                utils.delete_from_db(Department(name='Finance department'))

    def test_insert_into_db(self):
        """test adding a new department or an employee"""
        with self.context():
            dep = Department(id=150, name='Insert department')
            emp = Employee(id=150, fullname='Insert Employee',
                           bday=date(1994, 10, 23), salary=321, department_id=1)

            utils.insert_into_db(dep)
            utils.insert_into_db(emp)

            self.assertIn(dep, Department.query.all())
            self.assertIn(emp, Employee.query.all())

            with self.assertRaises(BadRequest):
                utils.insert_into_db('gsd')
                utils.insert_into_db(412)

            with self.assertRaises(InternalServerError):
                utils.insert_into_db(Department(name='Marketing department'))

            utils.delete_from_db(dep)
            utils.delete_from_db(emp)

    def test_update_department(self):
        """test updating a department"""
        with self.context():
            dep = Department(id=200, name='Update department')
            utils.insert_into_db(dep)

            utils.update_record(Department, dep, name='Super department')

            self.assertEqual(dep.name, 'Super department')

            utils.delete_from_db(dep)
            with self.assertRaises(BadRequest):
                utils.update_record(Department, 12, name='My department')
                utils.update_record('gas', dep, name='My department')
                utils.update_record(Department, dep)

    def test_update_employee(self):
        """test updating an employee"""
        with self.context():
            emp = Employee(id=200, fullname='Update Employee',
                           bday=date(1998, 11, 14), salary=312, department_id=1)
            utils.insert_into_db(emp)

            utils.update_record(Employee, emp, fullname='Super Employee', bday=date(2000, 2, 20), salary=500)

            self.assertEqual(emp.fullname, 'Super Employee')
            self.assertEqual(emp.bday, date(2000, 2, 20))
            self.assertEqual(int(emp.salary), 500)

            with self.assertRaises(BadRequest):
                utils.update_record(Employee, 12, name='My Employee')
                utils.update_record('gas', emp, name='My Employee')
                utils.update_record(Employee, emp)

            utils.delete_from_db(emp)

    def test_validate_employee_name(self):
        """test validating employee's name"""

        self.assertEqual(Employee.validate_fullname(''), False)
        self.assertEqual(Employee.validate_fullname('  '), False)
        self.assertEqual(Employee.validate_fullname('231312'), False)
        self.assertEqual(Employee.validate_fullname('fsad'), False)
        self.assertEqual(Employee.validate_fullname('dima 12321'), False)
        self.assertEqual(Employee.validate_fullname('Semen Volun'), True)
        self.assertEqual(Employee.validate_fullname('gasg gas'), True)
        self.assertEqual(Employee.validate_fullname(12412), False)

    def test_validate_department_name(self):
        """test validating department's name"""
        with self.context():
            self.assertEqual(Department.validate_name(''), False)
            self.assertEqual(Department.validate_name(' '), False)
            self.assertEqual(Department.validate_name('213'), False)
            self.assertEqual(Department.validate_name('123 fas '), False)
            self.assertEqual(Department.validate_name('Marketing'), False)
            self.assertEqual(Department.validate_name('Marketing department'), False)
            self.assertEqual(Department.validate_name('dep'), True)
            self.assertEqual(Department.validate_name('Management'), True)
            self.assertEqual(Department.validate_name('Managementdepartment'), False)
            self.assertEqual(Department.validate_name(213), False)

    def test_count_employees(self):
        """test counting the number of department's employees"""
        with self.context():
            dep = utils.get_or_404(Department, name='Marketing department')

            self.assertEqual(dep.number_of_employees(), 1)

    def test_average_salary(self):
        """test counting average department's salary"""
        with self.context():
            dep = utils.get_or_404(Department, name='Marketing department')

            self.assertEqual(dep.average_salary(), utils.get_or_404(Employee, department_id=dep.id).salary)
