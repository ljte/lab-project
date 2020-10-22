"""test rest api"""

import unittest
from datetime import date

from department_app.models import db
from department_app.service import utils
from department_app.models.department import Department
from department_app.models.employee import Employee
from department_app.config import TestConfig
from department_app import create_app


URL = 'http://localhost:5000/api'


class TestEmployeeRest(unittest.TestCase):
    """class for testing employee restful api"""

    @classmethod
    def setUpClass(cls):
        """setup db"""
        cls.app = create_app(app_config=TestConfig)
        cls.tester = cls.app.test_client()
        cls.context = cls.app.app_context
        with cls.context():
            db.create_all()
            utils.insert_into_db(Department(name='Management department'))
            utils.insert_into_db(Employee(fullname='Sergey Nemko',
                                          bday=date(1998, 12, 25), salary=555, department_id=1))

    def test_get_all_employees(self):
        """test getting all the employees"""
        with self.context():
            response = self.tester.get(f'{URL}/employees')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')
            self.assertDictEqual(response.json, {'employees': [emp.to_dict() for
                                                               emp in utils.get_all(Employee)]})

    def test_get_employee(self):
        """test getting a single employee"""
        with self.context():
            response = self.tester.get(f'{URL}/employees/1')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')
            self.assertDictEqual(response.json, utils.get_or_404(Employee, id=1).to_dict())

            self.assertEqual(self.tester.get(f'{URL}/employees/-1231').status_code, 404)
            self.assertEqual(self.tester.get(f'{URL}/employees/gasg').status_code, 404)

    def test_post_employee(self):
        """test creating a new employee"""
        with self.context():
            response = self.tester.post(f'{URL}/employees/',
                                        data={
                                              'fullname': 'Post Employee',
                                              'bday': date(1998, 12, 30),
                                              'salary': 500,
                                              'dep_name': 'Management department'
                                        })

            emp = utils.get_or_404(Employee, fullname='Post Employee')

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.content_type, 'application/json')
            self.assertIn(emp, utils.get_all(Employee))

            self.assertEqual(self.tester.post(f'{URL}/employees/',
                                              data={'fullname': ''}).status_code, 400)
            self.assertEqual(self.tester.post(f'{URL}/employees/').status_code, 400)
            self.assertEqual(self.tester.post(f'{URL}/employees/',
                                              data={
                                                  'fullname': '',
                                                  'bday': '1997-10-1',
                                                  'salary': 320,
                                                  'dep_name': 'Management department'
                                                }).status_code, 400)
            self.assertEqual(self.tester.post(f'{URL}/employees/',
                                              data={
                                                  'fullname': 'New Employee',
                                                  'bday': '1997-15-1',
                                                  'salary': 320,
                                                  'dep_name': 'Management department'
                                                }).status_code, 400)
            self.assertEqual(self.tester.post(f'{URL}/employees/',
                                              data={
                                                  'fullname': 'New Employee',
                                                  'bday': '1997-10-1',
                                                  'salary': 'gas',
                                                  'dep_name': 'Management department'
                                                }).status_code, 400)
            self.assertEqual(self.tester.post(f'{URL}/employees/',
                                              data={
                                                  'fullname': 'New Employee',
                                                  'bday': '1997-10-1',
                                                  'salary': 320,
                                                  'dep_name': ''
                                                }).status_code, 404)

            utils.delete_from_db(emp)

    def test_put_employee(self):
        """test updating an existing employee"""
        with self.context():
            emp = Employee(fullname='Update employee',
                           bday=date(1998, 10, 1), salary=312, department_id=1)
            utils.insert_into_db(emp)
            response = self.tester.put(f'{URL}/employees/{emp.id}',
                                       data={
                                           'fullname': 'Super employee',
                                           'bday': date(1995, 5, 5),
                                           'salary': 555
                                       })

            self.assertEqual(response.status_code, 204)
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(emp.fullname, 'Super employee')
            self.assertEqual(emp.bday, date(1995, 5, 5))
            self.assertEqual(emp.salary, 555)

            self.assertEqual(self.tester.put(f'{URL}/employees/').status_code, 400)
            self.assertEqual(self.tester.put(f'{URL}/employees/gsa',
                                             data={'fullname': 'new name'}).status_code, 404)
            self.assertEqual(self.tester.put(f'{URL}/employees/120031').status_code, 404)
            self.assertEqual(self.tester.put(f'{URL}/employees/1').status_code, 400)
            self.assertEqual(self.tester.put(f'{URL}/employees/1',
                                             data={'fullname': ''}).status_code, 400)
            self.assertEqual(self.tester.put(f'{URL}/employees/1',
                                             data={'salary': 'gsa'}).status_code, 400)
            self.assertEqual(self.tester.put(f'{URL}/employees/1',
                                             data={'bday': '1992-20-12'}).status_code, 400)
            self.assertEqual(self.tester.put(f'{URL}/employees/1',
                                             data={'dep_name': 'gsaas'}).status_code, 400)

            utils.delete_from_db(emp)

    def test_delete_employee(self):
        """test deleting an existing employee"""
        with self.context():
            emp = Employee(fullname='Delete employee',
                           bday=date(1999, 10, 11), salary=555, department_id=1)
            utils.insert_into_db(emp)

            response = self.tester.delete(f'{URL}/employees/{emp.id}')

            self.assertEqual(response.status_code, 204)
            self.assertEqual(response.content_type, 'application/json')

            self.assertNotIn(emp, utils.get_all(Department))

            self.assertEqual(self.tester.delete(f'{URL}/employees/').status_code, 400)
            self.assertEqual(self.tester.delete(f'{URL}/employees/-123').status_code, 404)
            self.assertEqual(self.tester.delete(f'{URL}/employees/gas').status_code, 404)
