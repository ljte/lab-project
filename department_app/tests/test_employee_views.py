"""test employee views"""

from unittest import mock
from datetime import date

from flask_testing import TestCase, LiveServerTestCase

from department_app import create_app
from department_app.config import LiveServerTest


class TestEmployeeViews(TestCase, LiveServerTestCase):
    """test employees views"""

    deps = [
        {
            'id': 1,
            'name': 'Marketing department',
            'average_salary': 673.0,
            'number_of_employees': 2
        },
        {
            'id': 2,
            'name': 'Management department',
            'average_salary': 534.0,
            'number_of_employees': 2
        },
        {
            'id': 3,
            'name': 'Finance department',
            'average_salary': 843.0,
            'number_of_employees': 1
        },
    ]
    emps = [
        {
            'id': 1,
            'fullname': 'Andrey Bosko',
            'bday': date(1992, 10, 25),
            'salary': 534,
            'department': 'Management department'
        },
        {
            'id': 2,
            'fullname': 'Semen Volkov',
            'bday': date(1985, 3, 13),
            'salary': 843,
            'department': 'Finance department'
        },
        {
            'id': 3,
            'fullname': 'Maksim Kolun',
            'bday': date(1989, 4, 20),
            'salary': 673,
            'department': 'Marketing department'
        }
    ]

    def create_app(self):
        return create_app(app_config=LiveServerTest)

    def setUp(self):
        self.url = f'{self.get_server_url()}/employees'

    def test_employee_main_page(self):
        """test that main page opens correctly"""
        response = self.client.get(self.url, follow_redirects=True)

        self.assertIn(b'Filter by birthday', response.data)
        self.assertIn(b'Filter by department', response.data)

    @mock.patch('requests.post')
    @mock.patch('requests.Response.json', side_effect=[
        {'employees': emps},
        {'departments': deps}
    ])
    def test_adding_employee_with_correct_input(self, mock_json, mock_response):
        """test that adding an employee works correctly"""
        mock_response.return_value.status_code = 201

        response = self.client.post(f'{self.url}/add',
                                    data={
                                        'fullname': 'Anna Volkova',
                                        'bday': date(1983, 9, 12),
                                        'salary': 732,
                                        'dep_name': 'Management department'
                                    }, follow_redirects=True)

        self.assertIn(b'Successfully added', response.data)

        mock_json.assert_called()
        mock_response.assert_called()

    @mock.patch('requests.Response.json', side_effect=[
        {'message': 'Invalid fullname'},
        {'departments': deps},
        {'message': 'Invalid fullname'},
        {'departments': deps},
        {'message': 'Invalid fullname'},
        {'departments': deps}
    ])
    def test_adding_employee_with_incorrect_fullname(self, mock_json):
        """test that adding an employee works correctly"""

        response = self.client.post(f'{self.url}/add',
                                    data={
                                        'fullname': '',
                                        'bday': date(1983, 9, 12),
                                        'salary': 732,
                                        'dep_name': 'Management department'
                                    }, follow_redirects=True)
        self.assertIn(b'Invalid fullname', response.data)

        response = self.client.post(f'{self.url}/add',
                                    data={
                                        'fullname': '12412',
                                        'bday': date(1983, 9, 12),
                                        'salary': 732,
                                        'dep_name': 'Management department'
                                    }, follow_redirects=True)
        self.assertIn(b'Invalid fullname', response.data)

        response = self.client.post(f'{self.url}/add',
                                    data={
                                        'fullname': 'asg',
                                        'bday': date(1983, 9, 12),
                                        'salary': 732,
                                        'dep_name': 'Management department'
                                    }, follow_redirects=True)
        self.assertIn(b'Invalid fullname', response.data)

        mock_json.assert_called()

    @mock.patch('requests.Response.json', side_effect=[
        {'message': 'Invalid birthday'},
        {'departments': deps},
        {'message': 'Invalid birthday'},
        {'departments': deps},
        {'message': 'Invalid birthday'},
        {'departments': deps}
    ])
    def test_adding_employee_with_incorrect_birthday(self, mock_json):
        """test that adding an employee with invalid bday works correctly"""

        response = self.client.post(f'{self.url}/add',
                                    data={
                                        'fullname': 'Anna Volkova',
                                        'bday': 123,
                                        'salary': 732,
                                        'dep_name': 'Management department'
                                    }, follow_redirects=True)
        self.assertIn(b'Invalid birthday', response.data)

        response = self.client.post(f'{self.url}/add',
                                    data={
                                        'fullname': 'Anna Volkova',
                                        'bday': '1998-23-10',
                                        'salary': 732,
                                        'dep_name': 'Management department'
                                    }, follow_redirects=True)
        self.assertIn(b'Invalid birthday', response.data)

        response = self.client.post(f'{self.url}/add',
                                    data={
                                        'fullname': 'Anna Volkova',
                                        'bday': '12-21-3231',
                                        'salary': 732,
                                        'dep_name': 'Management department'
                                    }, follow_redirects=True)
        self.assertIn(b'Invalid birthday', response.data)

        mock_json.assert_called()

    @mock.patch('requests.Response.json', side_effect=[
        {'message': 'Invalid salary'},
        {'departments': deps}
    ])
    def test_adding_employee_with_incorrect_salary(self, mock_json):
        """test that adding an employee with invalid salary type works correctly"""
        response = self.client.post(f'{self.url}/add',
                                    data={
                                        'fullname': 'Anna Volkova',
                                        'bday': date(1983, 9, 12),
                                        'salary': 'gasgsd',
                                        'dep_name': 'Management department'
                                    }, follow_redirects=True)
        self.assertIn(b'Invalid salary', response.data)

        mock_json.assert_called()

    @mock.patch('requests.Response.json', return_value={'departments': deps})
    def test_adding_employee_with_incorrect_department(self, mock_json):
        """test that adding an employee with invalid department works correctly"""
        response = self.client.post(f'{self.url}/add',
                                    data={
                                        'fullname': 'Anna Volkova',
                                        'bday': date(1983, 9, 12),
                                        'salary': 312,
                                    }, follow_redirects=True)
        self.assertIn(b'Choose a department', response.data)

        response = self.client.post(f'{self.url}/add',
                                    data={
                                        'fullname': 'Anna Volkova',
                                        'bday': date(1983, 9, 12),
                                        'salary': 312,
                                        'department': 1231
                                    }, follow_redirects=True)
        self.assertIn(b'Choose a department', response.data)

        mock_json.assert_called()

    @mock.patch('requests.get')
    @mock.patch('requests.put')
    def test_editing_employee_with_correct_values(self, mock_put_response, mock_get_response):
        """test that editing an employee works correctly"""
        mock_put_response.return_value.status_code = 204
        mock_get_response.return_value.status_code = 200

        response = self.client.post(f'{self.url}/edit/1',
                                    data={
                                        'fullname': 'Anna Bobrova',
                                        'bday': date(1999, 12, 31),
                                        'salary': 100,
                                        'department': 'Finance department'
                                    }, follow_redirects=True)
        self.assertIn(b'Successfully updated', response.data)

        mock_put_response.assert_called()
        mock_get_response.assert_called()

    @mock.patch('requests.get')
    @mock.patch('requests.Response.json', side_effect=[
        {'message': 'invalid name'}
    ])
    def test_editing_employee_with_invalid_fullname(self, mock_json, mock_get_response):
        """test that editing an employee works correctly"""
        self.emps[1]['bday'] = '13-03-1985'
        mock_get_response.return_value.status_code = 200
        mock_get_response.return_value.json.side_effect = [
            None,
            self.emps[1],
            {'departments': self.deps}
        ]

        response = self.client.post(f'{self.url}/edit/1',
                                    data={
                                        'fullname': ''
                                    }, follow_redirects=True)
        self.assertIn(b'invalid name', response.data)

        mock_get_response.assert_called()
        mock_json.assert_called()

    @mock.patch('requests.get')
    @mock.patch('requests.Response.json', side_effect=[
        {'message': 'invalid bday'}
    ])
    def test_editing_employee_with_invalid_birthday(self, mock_json, mock_get_response):
        """test that editing emp with invalid bday works correctly"""
        self.emps[1]['bday'] = '13-03-1985'
        mock_get_response.return_value.status_code = 200
        mock_get_response.return_value.json.side_effect = [
            None,
            self.emps[1],
            {'departments': self.deps}
        ]

        response = self.client.post(f'{self.url}/edit/1',
                                    data={
                                        'bday': '12-32-2313'
                                    }, follow_redirects=True)
        self.assertIn(b'invalid bday', response.data)

        mock_get_response.assert_called()
        mock_json.assert_called()

    @mock.patch('requests.get')
    @mock.patch('requests.Response.json', side_effect=[
        {'message': 'invalid salary'}
    ])
    def test_editing_employee_with_invalid_salary(self, mock_json, mock_get_response):
        """test that editing emp with invalid salary works correctly"""
        self.emps[1]['bday'] = '13-03-1985'
        mock_get_response.return_value.status_code = 200
        mock_get_response.return_value.json.side_effect = [
            None,
            self.emps[1],
            {'departments': self.deps}
        ]

        response = self.client.post(f'{self.url}/edit/1',
                                    data={
                                        'salary': 'gas'
                                    }, follow_redirects=True)
        self.assertIn(b'invalid salary', response.data)

        mock_get_response.assert_called()
        mock_json.assert_called()

    @mock.patch('requests.get')
    @mock.patch('requests.Response.json', side_effect=[
        {'message': 'invalid department'}
    ])
    def test_editing_employee_with_invalid_department(self, mock_json, mock_get_response):
        """test that editing emp with invalid department works correctly"""
        self.emps[1]['bday'] = '13-03-1985'
        mock_get_response.return_value.status_code = 200
        mock_get_response.return_value.json.side_effect = [
            None,
            self.emps[1],
            {'departments': self.deps}
        ]

        response = self.client.post(f'{self.url}/edit/1',
                                    data={
                                        'deparment': ''
                                    }, follow_redirects=True)
        self.assertIn(b'invalid department', response.data)

        mock_get_response.assert_called()
        mock_json.assert_called()

    @mock.patch('requests.Response.json', side_effect=[
        {'message': 'Employee was not found'},
        {'employees': emps},
        {'departments': deps},
    ])
    def test_editing_not_existing_employee(self, mock_json):
        """test that editing not existing emp works correctly"""

        response = self.client.post(f'{self.url}/edit/412412',
                                    data={
                                        'deparment': ''
                                    }, follow_redirects=True)
        self.assertIn(b'Employee was not found', response.data)

        mock_json.assert_called()

    @mock.patch('requests.delete')
    @mock.patch('requests.Response.json', side_effect=[
        emps[0],
        {'employees': emps},
        {'departments': deps},
    ])
    def test_deleting_employee(self, mock_json, mock_response):
        """test that deleting an employee works correctly"""
        mock_response.return_value.status_code = 204

        response = self.client.get(f'{self.url}/delete/1', follow_redirects=True)

        self.assertIn(b'Successfully deleted', response.data)

        mock_response.assert_called()
        mock_json.assert_called()

    @mock.patch('requests.Response.json', side_effect=[
        {'message': 'Employee was not found'},
        {'message': 'Employee was not found'},
        {'employees': emps},
        {'departments': deps},
    ])
    def test_deleting_not_existing_employee(self, mock_json):
        """test that deleting a not existing employee works correctly"""

        response = self.client.get(f'{self.url}/delete/122511212212412', follow_redirects=True)

        self.assertIn(b'Employee was not found', response.data)

        mock_json.assert_called()

    @mock.patch('requests.Response.json', side_effect=[
        {'employees': emps},
        {'departments': deps},
        {'employees': emps[:1]},
        {'departments': deps},
        {'employees': []},
        {'departments': deps},
    ])
    def test_searching_employees(self, mock_response):
        """test that searching an employee or employees works correctly"""

        response = self.client.get(f'{self.url}/search', data={'search_string': ''})

        self.assertIn(b'Andrey Bosko', response.data)
        self.assertIn(b'Semen Volkov', response.data)
        self.assertIn(b'Maksim Kolun', response.data)

        response = self.client.get(f'{self.url}/search', data={'search_string': 'Andrey'})

        self.assertIn(b'Andrey Bosko', response.data)
        self.assertNotIn(b'Semen Volkov', response.data)
        self.assertNotIn(b'Maksim Kolun', response.data)

        response = self.client.get(f'{self.url}/search', data={'search_string': '124'})

        self.assertNotIn(b'Andrey Bosko', response.data)
        self.assertNotIn(b'Semen Volkov', response.data)
        self.assertNotIn(b'Maksim Kolun', response.data)

        mock_response.assert_called()

    @mock.patch('requests.Response.json', side_effect=[
        {'departments': deps},
        {'employees': emps[:1]},
        {'departments': deps},
    ])
    def test_filtering_employees_by_bday(self, mock_response):
        """test that filtering employees  by bday works correctly"""
        response = self.client.post(f'{self.url}/filter_by_bday',
                                    data={'bday': '1992-10-25'},
                                    follow_redirects=True)

        self.assertIn(b'Andrey Bosko', response.data)
        self.assertNotIn(b'Semen Volkov', response.data)
        self.assertNotIn(b'Maksim Kolun', response.data)

        mock_response.assert_called()

    @mock.patch('requests.Response.json', side_effect=[
        {'departments': deps},
        {'message': 'Birthday must have YY-MM-DD format'},
        {'employees': emps},
        {'departments': deps},
    ])
    def test_filtering_employees_by_incorrect_bday(self, mock_response):
        """test that filtering employees by incorrect bday works correctly"""
        response = self.client.post(f'{self.url}/filter_by_bday',
                                    data={'bday': 12312},
                                    follow_redirects=True)

        self.assertIn(b'Birthday must have YY-MM-DD format', response.data)
        self.assertIn(b'Andrey Bosko', response.data)
        self.assertIn(b'Semen Volkov', response.data)
        self.assertIn(b'Maksim Kolun', response.data)

        mock_response.assert_called()

    @mock.patch('requests.get')
    def test_filtering_employees_by_bday_period(self, mock_response):
        """test that filtering employees by bday period works correctly"""
        mock_response.return_value.status_code = 200
        mock_response.return_value.json.side_effect = [
            {'departments': self.deps},
            {'employees': self.emps[1:]},
        ]
        response = self.client.post(f'{self.url}/filter_by_bday',
                                    data={'start_date': '1985-01-01',
                                          'end_date': '1990-31-12'},
                                    follow_redirects=True)

        self.assertNotIn(b'Andrey Bosko', response.data)
        self.assertIn(b'Semen Volkov', response.data)
        self.assertIn(b'Maksim Kolun', response.data)

        mock_response.assert_called()

    @mock.patch('requests.Response.json', side_effect=[
        {'departments': deps},
        {'message': 'Dates must have YY-MM-DD format'},
        {'employees': emps},
        {'departments': deps},
    ])
    def test_filtering_employees_by_incorrect_bday_period(self, mock_response):
        """test that filtering employees by bday period works correctly"""
        response = self.client.post(f'{self.url}/filter_by_bday',
                                    data={'start_date': 12312,
                                          'end_date': '1990-31-12'},
                                    follow_redirects=True)

        self.assertIn(b'Dates must have YY-MM-DD format', response.data)

        mock_response.assert_called()

    @mock.patch('requests.Response.json', side_effect=[
        {'departments': deps},
        {'employees': emps},
        {'departments': deps},
    ])
    def test_filtering_employees_with_no_dates(self, mock_response):
        """test that filtering employees by bday period works correctly"""
        response = self.client.post(f'{self.url}/filter_by_bday', follow_redirects=True)

        self.assertIn(b'You must specify both start and end dates or choose a birthday', response.data)

        mock_response.assert_called()

    @mock.patch('requests.Response.json', side_effect=[
        {'employees': emps},
        {'departments': deps},
        {'employees': emps},
        {'departments': deps},
        {'employees': emps},
        {'departments': deps},
    ])
    def test_filtering_by_department(self, mock_response):
        """test that filtering by department works correctly"""

        response = self.client.post(f'{self.url}/filter_by_department', follow_redirects=True)

        self.assertIn(b'Choose a department', response.data)

        response = self.client.post(f'{self.url}/filter_by_department',
                                    data={'department': 'Management department'},
                                    follow_redirects=True)
        self.assertIn(b'Andrey Bosko', response.data)
        self.assertNotIn(b'Semen Volkov', response.data)
        self.assertNotIn(b'Maksim Kolun', response.data)

        response = self.client.post(f'{self.url}/filter_by_department',
                                    data={'department': 123},
                                    follow_redirects=True)
        self.assertNotIn(b'Andrey Bosko', response.data)
        self.assertNotIn(b'Semen Volkov', response.data)
        self.assertNotIn(b'Maksim Kolun', response.data)

        mock_response.assert_called()
