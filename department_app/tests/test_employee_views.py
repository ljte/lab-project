"""test employee views"""

import unittest
from datetime import date

import requests

from department_app import create_app
from department_app.config import TestConfig


class TestEmployeeViews(unittest.TestCase):
    """class for testing employee views"""

    @classmethod
    def setUpClass(cls):
        """create app, test client and app context"""
        app = create_app(app_config=TestConfig)
        cls.tester = app.test_client()

    def test_main_employees_page(self):
        """test that /employees page loads correctly"""
        response = self.tester.get('/employees')

        assert b'Filter by birthday' in response.data
        assert b'Filter by department' in response.data

    def test_search_employee(self):
        """test that searching an employees by fullname works correctly"""
        response = self.tester.get('/employees/search', data={'search_string': 'Andrey'})

        assert b'Andrey Bobrov' in response.data
        assert b'Anna Volkova' not in response.data
        assert b'Boris Nemchenko' not in response.data
        assert b'Vladimir Novikov' not in response.data

    def test_filter_by_department(self):
        """test filtering employees by department """
        response = self.tester.post('/employees/filter_by_department', data={'department': 'Marketing department'})

        assert b'Boris Nemchenko' in response.data
        assert b'Vladimir Novikov' in response.data
        assert b'Andrey Bobrov' not in response.data
        assert b'Anna Volkova' not in response.data

    def test_filter_by_bday(self):
        """test filtering employees by birthday"""
        response = self.tester.post('/employees/filter_by_bday', data={'bday': '1992-06-23'})

        assert b'Andrey Bobrov' in response.data
        assert b'Anna Volkova' not in response.data
        assert b'Boris Nemchenko' not in response.data
        assert b'Vladimir Novikov' not in response.data

        response = self.tester.post('/employees/filter_by_bday', data={'bday': 1231}, follow_redirects=True)

        assert b'Birthday must have YY-MM-DD format' in response.data

        response = self.tester.post('/employees/filter_by_bday', follow_redirects=True)

        assert b'You must specify both start and end dates or choose a birthday' in response.data

    def test_filter_by_date_period(self):
        """test getting those employees whose birthday fall into
        the date period from start_date to end_date"""
        response = self.tester.post('/employees/filter_by_bday', data={'start_date': '1992-01-01',
                                                                       'end_date': '1993-12-31'})

        assert b'Andrey Bobrov' in response.data
        assert b'Boris Nemchenko' in response.data
        assert b'Anna Volkova' not in response.data
        assert b'Vladimir Novikov' not in response.data

        response = self.tester.post('/employees/filter_by_bday',
                                    data={'start_date': 124, 'end_date': '1993-12-31'},
                                    follow_redirects=True)
        assert b'Dates must have YY-MM-DD format' in response.data

        response = self.tester.post('/employees/filter_by_bday', data={'start_date': '1992-01-01',
                                                                       'end_date': 12331}, follow_redirects=True)
        assert b'Dates must have YY-MM-DD format' in response.data

        response = self.tester.post('/employees/filter_by_bday', follow_redirects=True)
        assert b'You must specify both start and end dates or choose a birthday' in response.data

    def test_edit_employee(self):
        """test that editing an employee works correctly"""
        emp = requests.get('http://localhost:5000/api/employees',
                           data={'search_string': 'edit'}).json()['employees'][0]

        response = self.tester.post(f"/employees/edit/{emp['id']}",
                                    data={'fullname': 'Updated Employee'},
                                    follow_redirects=True)
        assert b'Successfully updated' in response.data
        assert b'Updated Employee' in response.data

        response = self.tester.post('/employees/edit/2',
                                    data={'fullname': 123},
                                    follow_redirects=True)
        assert b"invalid employee&#39;s fullname" in response.data

        response = self.tester.post('/employees/edit/2',
                                    data={'salary': 'asfd'},
                                    follow_redirects=True)
        assert b"Failed to update" in response.data

        response = self.tester.post('/employees/edit/2',
                                    data={'department': 2231},
                                    follow_redirects=True)
        assert b"Failed to update" in response.data

        response = self.tester.post('/employees/edit/2',
                                    data={'bday': 1231},
                                    follow_redirects=True)
        assert b"Failed to update" in response.data

    def test_post_employee(self):
        """test that posting a new employee work well"""
        response = self.tester.post('/employees/add', data={
            'fullname': 'Add Employee',
            'salary': 312,
            'bday': date(1995, 12, 31),
            'dep_name': 'Marketing department'
        }, follow_redirects=True)

        assert b'Successfully added' in response.data
        assert b'Add Employee' in response.data

        response = self.tester.post('/employees/add', data={
            'fullname': 124,
            'salary': 312,
            'bday': date(1995, 12, 31),
            'dep_name': 'Marketing department'
        }, follow_redirects=True)
        assert b"invalid employee&#39;s name" in response.data

        response = self.tester.post('/employees/add', data={
            'fullname': 'New Employee',
            'salary': 'fas',
            'bday': date(1995, 12, 31),
            'dep_name': 'Marketing department'
        }, follow_redirects=True)
        assert b'could not convert' in response.data

        response = self.tester.post('/employees/add', data={
            'fullname': 'New Employee',
            'salary': 124,
            'bday': 1241,
            'dep_name': 'Marketing department'
        }, follow_redirects=True)
        assert b'does not match format &#39;%Y-%m-%d&#39;' in response.data

        response = self.tester.post('/employees/add', data={
            'fullname': 'New Employee',
            'salary': 124,
            'bday': date(1995, 12, 31),
            'dep_name': 312
        }, follow_redirects=True)
        assert b'was not found' in response.data

    def test_delete_employee(self):
        """test that deleting an employee works well"""

        response = self.tester.get("/employees/delete/1", follow_redirects=True)
        assert b'<td>One Employee</td>' not in response.data
        assert b'Succesfully deleted' in response.data

        response = self.tester.get("/employees/delete/121241512", follow_redirects=True)
        assert b'was not found' in response.data
