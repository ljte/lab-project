"""test department views"""

import unittest
from datetime import date

from department_app.models.department import Department, Employee
from department_app import create_app, db
from department_app.config import TestConfig
from department_app.service import utils


class TestViews(unittest.TestCase):
    """class for testing department views"""

    @classmethod
    def setUpClass(cls):
        """create app, test client and app context"""
        app = create_app(app_config=TestConfig)
        cls.tester = app.test_client()
        cls.context = app.app_context
        with cls.context():
            db.create_all()
            deps = [Department(name='Finance department'),
                    Department(name='Human Resource department'),
                    Department(name='Accounting department')]

            for dep in deps:
                utils.insert_into_db(dep)

            emps = [Employee(fullname='One Employee', salary=123, bday=date(1995, 12, 12), department_id=deps[0].id),
                    Employee(fullname='Two Employee', salary=700, bday=date(1995, 12, 12), department_id=deps[2].id),
                    Employee(fullname='Three Employee', salary=123, bday=date(1995, 12, 12), department_id=deps[1].id)]

            for emp in emps:
                utils.insert_into_db(emp)

    def test_main_departments_page(self):
        """test that the department's index page loads correctly"""
        with self.context():
            page = self.tester.get('/')

            assert page.status_code == 200
            assert b'Filter by the average salary' in page.data

    def test_correct_search_view(self):
        """test that search function works correctly"""
        with self.context():
            response = self.tester.get('/departments/search', data={'search_string': 'Finance'})

            assert response.status_code == 200

            assert b'Finance department' in response.data
            assert b'Human Resource department' not in response.data
            assert b'Accounting department' not in response.data

    def test_incorrect_search_view(self):
        """test that search function works correctly"""
        with self.context():
            response = self.tester.get('/departments/search', data={'search_string': 12312})

            assert response.status_code == 200

            assert b'Finance department' not in response.data
            assert b'Human Resource department' not in response.data
            assert b'Accounting department' not in response.data

    def test_edit_request(self):
        """test that editing a department works correctly"""
        with self.context():
            dep = utils.get_or_404(Department, name='Finance department')
            response = self.tester.post(f'/departments/edit/{dep.id}',
                                        data={'name': 'Updated department'},
                                        follow_redirects=True)
            assert b'Updated department' in response.data
            assert b'>Finance'not in response.data

            self.tester.post(f'/departments/edit/{dep.id}',
                             data={'name': 'Finance department'},
                             follow_redirects=True)

    def test_incorrect_edit_request(self):
        """test that editing a department works correctly"""
        with self.context():
            dep = utils.get_or_404(Department, name='Finance department')
            response = self.tester.post(f'/departments/edit/{dep.id}',
                                        data={'name': 1231},
                                        follow_redirects=True)
            assert b"invalid department&#39;s name" in response.data

            response = self.tester.post(f'/departments/edit/{dep.id}',
                                        data={'name': 'somedepartment'},
                                        follow_redirects=True)
            assert b"invalid department&#39;s name" in response.data

    def test_delete_view(self):
        """test that deleting a department works correctly"""
        with self.context():
            utils.insert_into_db(Department(name='Delete department'))
            dep = utils.get_or_404(Department, name='Delete department')
            response = self.tester.get(f'/departments/delete/{dep.id}', follow_redirects=True)

            assert b'>Delete department' not in response.data
            assert b'Succesfully deleted' in response.data

            response = self.tester.get('/departments/delete/44252312', follow_redirects=True)

            assert b'was not found' in response.data

    def test_post_view(self):
        """test that posting a new department works correctly"""
        with self.context():
            response = self.tester.post('/departments/add', data={'name': 'New department'},
                                        follow_redirects=True)

            assert b'Successfully added' in response.data
            assert b'New department' in response.data

            dep = utils.get_or_404(Department, name='New department')
            utils.delete_from_db(dep)

            response = self.tester.post('/departments/add', data={'name': 123},
                                        follow_redirects=True)
            assert b"invalid department&#39;s name" in response.data

    def test_filter_by_avg_salary_department(self):
        """test that filtering departments by avg salary works correctly"""
        with self.context():
            response = self.tester.post('/departments/filter_by_salary', data={'comparison': '>',
                                                                               'average_salary': 650})

            assert b'Accounting department' in response.data
            assert b'Finance department' not in response.data
            assert b'Human Resource department' not in response.data

            response = self.tester.post('/departments/filter_by_salary',
                                        data={'comparison': '>',
                                              'average_salary': 'agas'},
                                        follow_redirects=True)
            assert b'Invalid average salary' in response.data

            response = self.tester.post('/departments/filter_by_salary',
                                        data={'comparison': 'asdg',
                                              'average_salary': 123},
                                        follow_redirects=True)
            assert b'Invalid comparison operator' in response.data
