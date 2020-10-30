"""test rest api"""

from datetime import date
import unittest

from department_app.service import utils
from department_app.models import db
from department_app.models.employee import Employee
from department_app.models.department import Department
from department_app import create_app
from department_app.config import TestConfig


URL = 'http://localhost:5000/api'


class TestDeparmentRest(unittest.TestCase):
    """class for testing department restful api"""

    @classmethod
    def setUpClass(cls):
        """setup db"""
        cls.app = create_app(app_config=TestConfig)
        cls.context = cls.app.app_context
        cls.tester = cls.app.test_client()
        with cls.context():
            db.create_all()
            utils.insert_into_db(Department(name='Marketing department'))
            utils.insert_into_db(Employee(fullname='Sergey Nemko',
                                          bday=date(1998, 12, 25), salary=555, department_id=1))

    def test_get_all_departments(self):
        """test getting all the departments"""
        with self.context():
            response = self.tester.get(f'{URL}/departments')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')
            self.assertDictEqual(response.json, {'departments': [dep.to_dict() for
                                                                 dep in utils.get_all(Department)]})

    def test_get_department(self):
        """test getting a single department"""
        with self.context():
            response = self.tester.get(f'{URL}/departments/1')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')
            self.assertDictEqual(response.json, utils.get_or_404(Department, id=1).to_dict())

            self.assertEqual(self.tester.get(f'{URL}/departments/-1231').status_code, 404)
            self.assertEqual(self.tester.get(f'{URL}/departments/gasg').status_code, 404)
            self.assertEqual(self.tester.get(f'{URL}/departments/5345').status_code, 404)

    def test_post_department(self):
        """test creating a new department"""
        with self.context():
            response = self.tester.post(f'{URL}/departments/',
                                        data={'name': 'Post department'})

            dep = utils.get_or_404(Department, name='Post department')

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.content_type, 'application/json')
            self.assertIn(dep, utils.get_all(Department))

            self.assertEqual(self.tester.post(f'{URL}/departments/',
                                              data={'name': ''}).status_code, 400)
            self.assertEqual(self.tester.post(f'{URL}/departments/').status_code, 400)

            utils.delete_from_db(dep)

    def test_put_department(self):
        """test updating an existing department"""
        with self.context():
            dep = Department(name='Update department')
            utils.insert_into_db(dep)

            response = self.tester.put(f'{URL}/departments/{dep.id}', data={'name': 'Super department'})

            self.assertEqual(response.status_code, 204)
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(dep.name, 'Super department')

            self.assertEqual(self.tester.put(f'{URL}/departments/').status_code, 400)
            self.assertEqual(self.tester.put(f'{URL}/departments/gsa',
                                             data={'name': 'new name'}).status_code, 404)

            self.assertEqual(self.tester.put(f'{URL}/departments/120031').status_code, 400)
            self.assertEqual(self.tester.put(f'{URL}/departments/1').status_code, 400)
            self.assertEqual(self.tester.put(f'{URL}/departments/1',
                                             data={'name': ''}).status_code, 400)

            utils.delete_from_db(dep)

    def test_delete_department(self):
        """test deleting an existing department"""
        with self.context():
            dep = Department(name='Deletethis department')
            utils.insert_into_db(dep)

            response = self.tester.delete(f'{URL}/departments/{dep.id}')

            self.assertEqual(response.status_code, 204)
            self.assertEqual(response.content_type, 'application/json')

            self.assertNotIn(dep, utils.get_all(Department))

            self.assertEqual(self.tester.delete(f'{URL}/departments/').status_code, 400)
            self.assertEqual(self.tester.delete(f'{URL}/departments/-123').status_code, 404)
            self.assertEqual(self.tester.delete(f'{URL}/departments/gas').status_code, 404)
            self.assertEqual(self.tester.delete(f'{URL}/departments/645645').status_code, 404)

            dep = utils.get_or_404(Department, name='Marketing department')
            self.assertEqual(self.tester.delete(f'{URL}/departments/{dep.id}').status_code, 400)
