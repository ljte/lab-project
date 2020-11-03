"""test department views"""

import unittest

import requests

from department_app import create_app
from department_app.config import TestConfig


class TestDepartmentViews(unittest.TestCase):
    """class for testing department views"""

    @classmethod
    def setUpClass(cls):
        """create app, test client and app context"""
        app = create_app(app_config=TestConfig)
        cls.tester = app.test_client()

    def test_main_departments_page(self):
        """test that the department's index page loads correctly"""
        page = self.tester.get('/')
        assert page.status_code == 200
        assert b'Filter by the average salary' in page.data

    def test_correct_search_view(self):
        """test that search function works correctly"""
        response = self.tester.get('/departments/search', data={'search_string': 'Finance'})

        assert response.status_code == 200

        assert b'Finance department' in response.data
        assert b'Human Resource department' not in response.data
        assert b'Accounting department' not in response.data

    def test_incorrect_search_view(self):
        """test that search function works correctly"""
        response = self.tester.get('/departments/search', data={'search_string': 12312})

        assert response.status_code == 200

        assert b'Finance department' not in response.data
        assert b'Human Resource department' not in response.data
        assert b'Accounting department' not in response.data

    def test_edit_request(self):
        """test that editing a department works correctly"""
        dep = requests.get('http://localhost:5000/api/departments',
                           data={'search_string': 'edit'}).json()['departments'][0]

        response = self.tester.post(f"/departments/edit/{dep['id']}",
                                    data={'name': 'Updated department'},
                                    follow_redirects=True)

        assert b'Updated department' in response.data
        assert b'<td>Edit department</td>'not in response.data

        response = self.tester.post("/departments/edit/124124",
                                    data={'name': 'Updated department'},
                                    follow_redirects=True)
        assert b"was not found" in response.data

    def test_incorrect_edit_request(self):
        """test that editing a department works correctly"""
        response = self.tester.post("/departments/edit/1",
                                    data={'name': 1231},
                                    follow_redirects=True)
        assert b"invalid department&#39;s name" in response.data

        response = self.tester.post("/departments/edit/1",
                                    data={'name': 'somedepartment'},
                                    follow_redirects=True)
        assert b"invalid department&#39;s name" in response.data

    def test_delete_view(self):
        """test that deleting a department works correctly"""
        dep = requests.get('http://localhost:5000/api/departments',
                           data={'search_string': 'delete'}).json()['departments'][0]

        response = self.tester.get(f"/departments/delete/{dep['id']}", follow_redirects=True)
        assert b'Succesfully deleted' in response.data
        assert b'<td>Delete department</td>' not in response.data

        response = self.tester.get('/departments/delete/44252312', follow_redirects=True)
        assert b'was not found' in response.data

    def test_post_view(self):
        """test that posting a new department works correctly"""
        response = self.tester.post('/departments/add', data={'name': 'New department'},
                                    follow_redirects=True)

        assert b'Successfully added' in response.data
        assert b'New department' in response.data

        response = self.tester.post('/departments/add', data={'name': 123},
                                    follow_redirects=True)
        assert b"invalid department&#39;s name" in response.data

    def test_filter_by_avg_salary_department(self):
        """test that filtering departments by avg salary works correctly"""
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
                                    data={'comparison': 'asd',
                                          'average_salary': 123},
                                    follow_redirects=True)
        assert b'Wrong comparison operator' in response.data

        response = self.tester.get('/departments/filter_by_salary', follow_redirects=True)
        assert b'Filter by the average salary' in response.data
