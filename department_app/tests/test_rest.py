import unittest
from datetime import date

from department_app import service
from department_app.models import Department, Employee

from requests import get, post, put, delete


service.reload_db()
url = 'http://localhost:5000/api'


class TestRest(unittest.TestCase):

    def test_get_department(self):
        response = get(f'{url}/departments/1')
        dep = response.json()

        self.assertEqual(dep['name'], Department.query.filter_by(id=1).first().name)
        self.assertEqual(response.status_code, 200)

        self.assertDictEqual(get(f'{url}/departments/').json(),
                             {'departments': [dep.to_dict() for dep in Department.query.all()]})

        self.assertEqual(get(f'{url}/departments/gsag').status_code, 400)
        self.assertEqual(get(f'{url}/departments/423423423432').status_code, 404)

    def test_post_department(self):
        response = post(f'{url}/departments', data={'dep_name': 'Some department'})
        dep = response.json()

        self.assertIn(Department.query.filter_by(name=dep['name']).first(),
                      Department.query.all())
        self.assertEqual(response.status_code, 201)

        self.assertEqual(post(f'{url}/departments').status_code, 400)
        self.assertEqual(post(f'{url}/departments', data={'fsadfsa': 3423}).status_code, 400)
        self.assertEqual(post(f'{url}/departments', data={'dep_name': 3423}).status_code, 400)
        self.assertEqual(post(f'{url}/departments', data={'dep_name': '    '}).status_code, 400)
        self.assertEqual(post(f'{url}/departments', data={'dep_name': ''}).status_code, 400)
        self.assertEqual(post(f'{url}/departments', data={'dep_name': 'Marketing department'}).status_code, 400)

    def test_put_department(self):
        response = put(f'{url}/departments/1', data={'dep_name': 'Test'})
        dep = response.json()

        self.assertEqual(dep['name'], Department.query.filter_by(id=1).first().name)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(put(f'{url}/departments/1').status_code, 400)
        self.assertEqual(put(f'{url}/departments/1', data={'asgagsd': 431421}).status_code, 400)
        self.assertEqual(put(f'{url}/departments/1', data={'dep_name:': 412412}).status_code, 400)
        self.assertEqual(put(f'{url}/departments/1', data={'dep_name:': 'Marketing'}).status_code, 400)
        self.assertEqual(put(f'{url}/departments/52325', data={'dep_name:': 'Some department'}).status_code, 404)
        self.assertEqual(put(f'{url}/departments/gsdgsd', data={'dep_name:': 'Some department'}).status_code, 400)
        self.assertEqual(put(f'{url}/departments/', data={'dep_name:': 'Some department'}).status_code, 400)

    def test_delete_department(self):
        dep = Department.query.all()[-1]
        response = delete(f'{url}/departments/{dep.id}')

        self.assertNotIn(dep, Department.query.all())
        self.assertEqual(response.status_code, 204)

        self.assertEqual(delete(f'{url}/departments/52325').status_code, 404)
        self.assertEqual(delete(f'{url}/departments/gsdgsd').status_code, 400)
        self.assertEqual(put(f'{url}/departments/').status_code, 400)

    def test_get_employee(self):
        response = get(f'{url}/employees/1')
        emp = response.json()

        self.assertEqual(emp['id'], Employee.query.filter_by(id=1).first().id)
        self.assertEqual(response.status_code, 200)

        self.assertDictEqual(get(f'{url}/employees/').json(),
                             {'employees': [emp.to_dict() for emp in Employee.query.all()]})

        self.assertEqual(get(f'{url}/employees/412421').status_code, 404)
        self.assertEqual(get(f'{url}/employees/fasfa').status_code, 400)

    def test_post_employee(self):
        response = post(f'{url}/employees/', data={
            'fullname': 'Semen Volkov',
            'bday': date(1999, 10, 25),
            'salary': 932.32,
            'dep_name': 'Management department'
        })

        self.assertIn(Employee.query.filter_by(fullname='Semen Volkov').first(),
                      Employee.query.all())
        self.assertEqual(response.status_code, 201)

        self.assertEqual(post(f'{url}/employees/').status_code, 400)
        self.assertEqual(post(f'{url}/employees/', data={'gas': 'gas'}).status_code, 400)
        self.assertEqual(post(f'{url}/employees/', data={'fullname': 'gas'}).status_code, 400)
        self.assertEqual(post(f'{url}/employees/', data={'fullname': 'gas',
                                                         'bday': '2000-10-25',
                                                         'salary': 421.4,
                                                         'dep_name': 'Marketing department'}).status_code, 400)
        self.assertEqual(post(f'{url}/employees/', data={'fullname': 'Dima Semenov',
                                                         'bday': '2000-15-25',
                                                         'salary': 421.4,
                                                         'dep_name': 'Marketing department'}).status_code, 400)
        self.assertEqual(post(f'{url}/employees/', data={'fullname': 'gas',
                                                         'bday': '2000-10-25',
                                                         'salary': 'fas',
                                                         'dep_name': 'Marketing department'}).status_code, 400)

    def test_put_employee(self):
        response = put(f'{url}/employees/1', data={
            'fullname': 'Anna Volkova',
            'bday': '1996-8-25',
            'salary': 754,
            'dep_name': 'Marketing department'
        })
        emp = Employee.query.filter_by(id=1).first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(emp.fullname, 'Anna Volkova')
        self.assertEqual(emp.bday, date(1996, 8, 25))
        self.assertEqual(emp.salary, 754)
        self.assertEqual(emp.department.name, 'Marketing department')

        self.assertEqual(put(f'{url}/employees/1', data={'fsfas': 213421}).status_code, 400)
        self.assertEqual(put(f'{url}/employees/1', data={'fullname': '312312'}).status_code, 400)
        self.assertEqual(put(f'{url}/employees/1', data={'fullname': '312 312'}).status_code, 400)
        self.assertEqual(put(f'{url}/employees/1', data={'bday': '20-23-3244'}).status_code, 400)
        self.assertEqual(put(f'{url}/employees/1', data={'bday': '3244-23-20'}).status_code, 400)
        self.assertEqual(put(f'{url}/employees/1', data={'bday': '1998-13-20'}).status_code, 400)
        self.assertEqual(put(f'{url}/employees/1', data={'bday': '1998-12-35'}).status_code, 400)
        self.assertEqual(put(f'{url}/employees/1', data={'salary': 'asgs'}).status_code, 400)
        self.assertEqual(put(f'{url}/employees/1', data={'dep_name': 'gagas'}).status_code, 400)
        self.assertEqual(put(f'{url}/employees/1', data={'dep_name': '412 department'}).status_code, 400)

    def test_delete_employee(self):
        emp = Employee.query.all()[-1]

        response = delete(f"{url}/employees/{emp.id}")

        self.assertEqual(response.status_code, 204)
        self.assertNotIn(emp, Employee.query.all())

        self.assertEqual(delete(f"{url}/employees/fasgas").status_code, 400)
        self.assertEqual(delete(f"{url}/employees/1412981248").status_code, 404)


if __name__ == "__main__":
    unittest.main()
