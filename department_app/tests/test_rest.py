"""test rest api"""

import unittest
from datetime import date

from department_app import service, app, db
from department_app.models import Department, Employee
from department_app.config import  TestConfig


url = 'http://localhost:5000/api'


class TestRest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config.from_object(TestConfig)
        db.create_all()
        service.insert_into_db(Department(id=1, name='Management department'))
        service.insert_into_db(Employee(id=1, fullname='Sergey Nemko',
                                        bday=date(1998, 12, 25), salary=555, department_id=1))
        cls.tester = app.test_client()

    def test_get_all_departments(self):

        response = self.tester.get(f'{url}/departments')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertDictEqual(response.json, {'departments': [dep.to_dict() for
                                                             dep in service.get_all(Department)]})

    def test_get_department(self):

        response = self.tester.get(f'{url}/departments/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertDictEqual(response.json, service.get_or_404(Department, id=1).to_dict())

        self.assertEqual(self.tester.get(f'{url}/departments/-1231').status_code, 404)
        self.assertEqual(self.tester.get(f'{url}/departments/gasg').status_code, 404)

    def test_post_department(self):

        response = self.tester.post(f'{url}/departments/', data={'id': 333, 'name': 'Post department'})

        dep = service.get_or_404(Department, id=333)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIn(dep, service.get_all(Department))

        self.assertEqual(self.tester.post(f'{url}/departments/', data={'id': 333, 'name': ''}).status_code, 400)
        self.assertEqual(self.tester.post(f'{url}/departments/').status_code, 400)

        service.delete_from_db(dep)

    def test_put_department(self):

        dep = Department(id=500, name='Update department')
        service.insert_into_db(dep)

        response = self.tester.put(f'{url}/departments/500', data={'name': 'Super department'})

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(dep.name, 'Super department')

        self.assertEqual(self.tester.put(f'{url}/departments/').status_code, 400)
        self.assertEqual(self.tester.put(f'{url}/departments/gsa', data={'name': 'new name'}).status_code, 404)
        self.assertEqual(self.tester.put(f'{url}/departments/120031').status_code, 400)
        self.assertEqual(self.tester.put(f'{url}/departments/1').status_code, 400)
        self.assertEqual(self.tester.put(f'{url}/departments/1', data={'name': ''}).status_code, 400)

        service.delete_from_db(dep)

    def test_delete_department(self):

        dep = Department(id=501, name='Delete department')
        service.insert_into_db(dep)

        response = self.tester.delete(f'{url}/departments/501')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content_type, 'application/json')

        self.assertNotIn(dep, service.get_all(Department))

        self.assertEqual(self.tester.delete(f'{url}/departments/').status_code, 400)
        self.assertEqual(self.tester.delete(f'{url}/departments/-123').status_code, 404)
        self.assertEqual(self.tester.delete(f'{url}/departments/gas').status_code, 404)

    def test_get_all_employees(self):

        response = self.tester.get(f'{url}/employees')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertDictEqual(response.json, {'employees': [emp.to_dict() for
                                                           emp in service.get_all(Employee)]})

    def test_get_employee(self):

        response = self.tester.get(f'{url}/employees/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertDictEqual(response.json, service.get_or_404(Employee, id=1).to_dict())

        self.assertEqual(self.tester.get(f'{url}/employees/-1231').status_code, 404)
        self.assertEqual(self.tester.get(f'{url}/employees/gasg').status_code, 404)

    def test_post_employee(self):

        response = self.tester.post(f'{url}/employees/', data={'id': 333,
                                                               'fullname': 'Post Employee',
                                                               'bday': date(1998, 12, 30),
                                                               'salary': 500,
                                                               'dep_name': 'Management department'})

        emp = service.get_or_404(Employee, id=333)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, 'application/json')
        self.assertIn(emp, service.get_all(Employee))

        self.assertEqual(self.tester.post(f'{url}/employees/', data={'fullname': ''}).status_code, 400)
        self.assertEqual(self.tester.post(f'{url}/employees/').status_code, 400)
        self.assertEqual(self.tester.post(f'{url}/employees/', data={'fullname': '',
                                                                     'bday': '1997-10-1',
                                                                     'salary': 320,
                                                                     'dep_name': 'Management department'
                                                                     }).status_code, 400)
        self.assertEqual(self.tester.post(f'{url}/employees/', data={'fullname': 'New Employee',
                                                                     'bday': '1997-15-1',
                                                                     'salary': 320,
                                                                     'dep_name': 'Management department'
                                                                     }).status_code, 400)
        self.assertEqual(self.tester.post(f'{url}/employees/', data={'fullname': 'New Employee',
                                                                     'bday': '1997-10-1',
                                                                     'salary': 'gas',
                                                                     'dep_name': 'Management department'
                                                                     }).status_code, 400)
        self.assertEqual(self.tester.post(f'{url}/employees/', data={'fullname': 'New Employee',
                                                                     'bday': '1997-10-1',
                                                                     'salary': 320,
                                                                     'dep_name': ''
                                                                     }).status_code, 404)

        service.delete_from_db(emp)

    def test_put_employee(self):

        emp = Employee(id=500, fullname='Update employee',
                       bday=date(1998, 10, 1), salary=312, department_id=1)
        service.insert_into_db(emp)
        response = self.tester.put(f'{url}/employees/500', data={'fullname': 'Super employee',
                                                                 'bday': date(1995, 5, 5),
                                                                 'salary': 555})

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(emp.fullname, 'Super employee')
        self.assertEqual(emp.bday, date(1995, 5, 5))
        self.assertEqual(emp.salary, 555)

        self.assertEqual(self.tester.put(f'{url}/employees/').status_code, 400)
        self.assertEqual(self.tester.put(f'{url}/employees/gsa', data={'fullname': 'new name'}).status_code, 404)
        self.assertEqual(self.tester.put(f'{url}/employees/120031').status_code, 404)
        self.assertEqual(self.tester.put(f'{url}/employees/1').status_code, 400)
        self.assertEqual(self.tester.put(f'{url}/employees/1', data={'fullname': ''}).status_code, 400)
        self.assertEqual(self.tester.put(f'{url}/employees/1', data={'salary': 'gsa'}).status_code, 400)
        self.assertEqual(self.tester.put(f'{url}/employees/1', data={'bday': '1992-20-12'}).status_code, 400)
        self.assertEqual(self.tester.put(f'{url}/employees/1', data={'dep_name': 'gsaas'}).status_code, 400)

        service.delete_from_db(emp)

    def test_delete_employee(self):

        emp = Employee(id=1000, fullname='Delete employee',
                       bday=date(1999, 10, 11), salary=555, department_id=1)
        service.insert_into_db(emp)

        response = self.tester.delete(f'{url}/employees/1000')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content_type, 'application/json')

        self.assertNotIn(emp, service.get_all(Department))

        self.assertEqual(self.tester.delete(f'{url}/employees/').status_code, 400)
        self.assertEqual(self.tester.delete(f'{url}/employees/-123').status_code, 404)
        self.assertEqual(self.tester.delete(f'{url}/employees/gas').status_code, 404)


if __name__ == "__main__":
    unittest.main()
