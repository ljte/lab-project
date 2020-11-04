"""test department views"""

from unittest import mock

from flask_testing import LiveServerTestCase, TestCase

from department_app import create_app, db
from department_app.config import TestConfig


class TestDepartmentViews(TestCase, LiveServerTestCase):
    """test department views"""

    deps = [
        {
            'id': 1,
            'name': 'Marketing department',
            'average_salary': 500.0,
            'number_of_employees': 1
        },
        {
            'id': 2,
            'name': 'Management department',
            'average_salary': 453.0,
            'number_of_employees': 1
        },
        {
            'id': 3,
            'name': 'Finance department',
            'average_salary': 0.0,
            'number_of_employees': 0
        },
    ]

    def create_app(self):
        app = create_app(app_config=TestConfig)
        with app.app_context():
            db.create_all()
        return app

    @mock.patch('requests.Response.json', return_value={'departments': deps})
    def test_main_page(self, mock_departments):
        """test that main page opens correctly"""
        response = self.client.get(self.get_server_url(), follow_redirects=True)

        self.assert200(response)
        self.assertIn(b'Filter by the average salary', response.data)

        mock_departments.assert_called_once()

    @mock.patch('requests.post')
    @mock.patch('requests.Response.json', return_value={'departments': deps})
    def test_add_department_with_correct_input(self, mock_json, mock_response):
        """test adding a department with correct values"""
        mock_response.return_value.status_code = 201
        url = self.get_server_url()
        response = self.client.post(f'{url}/departments/add',
                                    data={'name': 'Accounting department'},
                                    follow_redirects=True)

        self.assertIn(b'Successfully added', response.data)

        mock_response.assert_called()
        mock_json.assert_called()

    def test_add_department_with_incorrect_input(self):
        """test adding a department with incorrect values"""
        url = self.get_server_url()
        response = self.client.post(f'{url}/departments/add',
                                    data={'name': 12312},
                                    follow_redirects=True)
        self.assertIn(b'invalid department&#39;s name', response.data)

        response = self.client.post(f'{url}/departments/add',
                                    data={'name': 'somedepartment'},
                                    follow_redirects=True)
        self.assertIn(b'invalid department&#39;s name', response.data)

        response = self.client.post(f'{url}/departments/add',
                                    data={'name': ''},
                                    follow_redirects=True)
        self.assertIn(b'invalid department&#39;s name', response.data)

    @mock.patch('requests.delete')
    @mock.patch('requests.Response.json', side_effect=[deps[2], {'departments': deps}])
    def test_deleting_existing_department(self, mock_json, mock_response):
        """test that deleting an existing department works correctly"""
        mock_response.return_value.status_code = 204

        url = self.get_server_url()
        response = self.client.get(f'{url}/departments/delete/3', follow_redirects=True)

        self.assertIn(b'Successfully deleted', response.data)

        mock_json.assert_called()
        mock_response.assert_called()

    @mock.patch('requests.Response.json', side_effect=[
        None,
        {'message': 'Department was not found'},
        {'departments': deps}
    ])
    def test_deleting_not_existing_department(self, mock_json):
        """test that deleting a non existing department works correctly"""

        url = self.get_server_url()
        response = self.client.get(f'{url}/departments/delete/125252353215213', follow_redirects=True)

        self.assertIn(b'Department was not found', response.data)

        mock_json.assert_called()

    @mock.patch('requests.Response.json', side_effect=[
        None,
        {'message': 'Department must have 0 employees to be deleted'},
        {'departments': deps}
    ])
    def test_deleting_department_with_employees(self, mock_json):
        """test that deleting a department with employees works correctly"""

        url = self.get_server_url()
        response = self.client.get(f'{url}/departments/delete/1', follow_redirects=True)

        self.assertIn(b'Department must have 0 employees to be deleted', response.data)

        mock_json.assert_called()

    @mock.patch('requests.get')
    @mock.patch('requests.put')
    def test_editing_department_with_correct_input(self, mock_put_response, mock_get_response):
        """test that editing a department work correctly"""
        mock_put_response.return_value.status_code = 204
        mock_get_response.return_value.status_code = 200
        url = self.get_server_url()

        response = self.client.post(f'{url}/departments/edit/1',
                                    data={'name': 'New department'},
                                    follow_redirects=True)

        self.assertIn(b'Successfully changed', response.data)

        mock_get_response.assert_called()
        mock_put_response.assert_called()

    @mock.patch('requests.Response.json', side_effect=[
        {'message': 'Department was not found'},
        {'departments': deps}
    ])
    def test_editing_not_existind_department(self, mock_json):
        """test that editing a department work correctly"""
        url = self.get_server_url()

        response = self.client.post(f'{url}/departments/edit/12412412',
                                    data={'name': 'New department'},
                                    follow_redirects=True)

        self.assertIn(b'Department was not found', response.data)

        mock_json.assert_called()

    @mock.patch('requests.get')
    @mock.patch('requests.Response.json', return_value={'message': "invalid department's name"})
    def test_editing_existind_department_with_incorrect_input(self, mock_json, mock_get_response):
        """test that editing a department work correctly"""
        mock_get_response.return_value.status_code = 200
        url = self.get_server_url()

        response = self.client.post(f'{url}/departments/edit/1',
                                    data={'name': 12412},
                                    follow_redirects=True)
        self.assertIn(b"invalid department&#39;s name", response.data)

        response = self.client.post(f'{url}/departments/edit/1',
                                    data={'name': 'newdepartment'},
                                    follow_redirects=True)
        self.assertIn(b"invalid department&#39;s name", response.data)

        response = self.client.post(f'{url}/departments/edit/1',
                                    data={'name': ''},
                                    follow_redirects=True)
        self.assertIn(b"invalid department&#39;s name", response.data)

        mock_json.assert_called()

    @mock.patch('requests.Response.json', side_effect=[
        {'departments': [deps[1]]},
        {'departments': deps},
        {'departments': []}
    ])
    def test_searching_deparment(self, mock_response):
        """test that searhing a department works correctly"""
        url = self.get_server_url()
        response = self.client.get(f'{url}/departments/search', data={'search_string': 'Management'})
        self.assertIn(b">Management department", response.data)
        self.assertNotIn(b">Marketing department", response.data)
        self.assertNotIn(b">Finance department", response.data)

        response = self.client.get(f'{url}/departments/search', data={'search_string': ''})
        self.assertIn(b">Management department", response.data)
        self.assertIn(b">Marketing department", response.data)
        self.assertIn(b">Finance department", response.data)

        response = self.client.get(f'{url}/departments/search', data={'search_string': '123'})
        self.assertNotIn(b">Management department", response.data)
        self.assertNotIn(b">Marketing department", response.data)
        self.assertNotIn(b">Finance department", response.data)

        mock_response.assert_called()

    @mock.patch('requests.Response.json', return_value={'departments': deps})
    def test_filtering_departments_by_average_salary(self, mock_response):
        """test that filtering the department works correrctly"""
        url = self.get_server_url()
        response = self.client.post(f'{url}/departments/filter_by_salary',
                                    data={
                                        'comparison': '=',
                                        'average_salary': 500
                                    })
        self.assertIn(b'Marketing department', response.data)
        self.assertNotIn(b'Management department', response.data)
        self.assertNotIn(b'Finance department', response.data)

        response = self.client.post(f'{url}/departments/filter_by_salary',
                                    data={
                                        'comparison': '<',
                                        'average_salary': 500
                                    })
        self.assertNotIn(b'Marketing department', response.data)
        self.assertIn(b'Management department', response.data)
        self.assertIn(b'Finance department', response.data)

        response = self.client.post(f'{url}/departments/filter_by_salary',
                                    data={
                                        'comparison': '>=',
                                        'average_salary': 0
                                    })
        self.assertIn(b'Marketing department', response.data)
        self.assertIn(b'Management department', response.data)
        self.assertIn(b'Finance department', response.data)

        mock_response.assert_called()

    @mock.patch('requests.Response.json', return_value={'departments': deps})
    def test_filtering_departments_with_incorrect_input_by_average_salary(self, mock_response):
        """test that filtering the department works correrctly"""
        url = self.get_server_url()
        response = self.client.post(f'{url}/departments/filter_by_salary',
                                    data={
                                        'comparison': 1231,
                                        'average_salary': 500
                                    }, follow_redirects=True)
        self.assertIn(b'Wrong comparison operator', response.data)

        response = self.client.post(f'{url}/departments/filter_by_salary',
                                    data={
                                        'comparison': 'aasd',
                                        'average_salary': 500
                                    }, follow_redirects=True)
        self.assertIn(b'Wrong comparison operator', response.data)

        response = self.client.post(f'{url}/departments/filter_by_salary',
                                    data={
                                        'comparison': '>',
                                        'average_salary': 'dgsa'
                                    }, follow_redirects=True)
        self.assertIn(b'Invalid average salary', response.data)

        response = self.client.post(f'{url}/departments/filter_by_salary',
                                    data={
                                        'comparison': '>',
                                        'average_salary': ''
                                    }, follow_redirects=True)
        self.assertIn(b'Invalid average salary', response.data)


        mock_response.assert_called()
