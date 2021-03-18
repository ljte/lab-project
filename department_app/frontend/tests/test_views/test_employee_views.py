from unittest import mock

from django.test import Client, TestCase

json_departments = [
    {
        "id": 1,
        "name": "Marketing department",
        "number_of_employees": 2,
        "average_salary": 4324.42,
    },
    {
        "id": 2,
        "name": "Management department",
        "number_of_employees": 4,
        "average_salary": 8234.234,
    },
]

json_employees = [
    {
        "id": 1,
        "fullname": "Andrey Borsuk",
        "salary": 4234.3,
        "bday": "1982-12-25",
        "department": "Marketing department",
    },
    {
        "id": 2,
        "fullname": "Anna Volkova",
        "salary": 1323.2,
        "bday": "1992-10-12",
        "department": "Management department",
    },
]


class TestEmployeeViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_employees_page(self):
        with mock.patch("requests.get") as mock_req:
            mock_req.return_value.status_code = 200
            mock_req.return_value.json.side_effect = [json_employees, json_departments]
            resp = self.client.get("/employees/")
        self.assertTemplateUsed(resp, "employees/employees.html")
        self.assertIn(b"Andrey Borsuk", resp.content)

    def test_post_employee(self):
        with mock.patch("requests.post") as mock_req:
            with mock.patch("requests.get") as mock_get:
                mock_req.return_value.status_code = 201
                mock_get.return_value.status_code = 200
                mock_get.return_value.json.side_effect = [
                    json_departments,
                    json_employees,
                    json_departments,
                ]
                resp = self.client.post(
                    "/add_employee/", json_employees[0], follow=True
                )
        self.assertTemplateUsed(resp, "employees/employees.html")
        self.assertIn(b"Successfully added Andrey Borsuk", resp.content)

    def test_put_employee(self):
        with mock.patch("requests.put") as mock_req:
            with mock.patch("requests.get") as mock_get:
                mock_req.return_value.status_code = 204
                mock_get.return_value.status_code = 200
                mock_get.return_value.json.side_effect = [
                    json_employees[0],
                    json_departments,
                    json_employees,
                    json_departments,
                ]
                resp = self.client.post(
                    "/edit_employee/1", {"fullname": "Semen Borsuk"}, follow=True
                )
        self.assertTemplateUsed(resp, "employees/employees.html")
        self.assertIn(b"Successfully edited Andrey Borsuk", resp.content)

    def test_delete_employee(self):
        with mock.patch("requests.delete") as mock_req:
            with mock.patch("requests.get") as mock_get:
                mock_req.return_value.status_code = 200
                mock_req.return_value.json.return_value = json_employees[0]
                mock_get.return_value.status_code = 200
                mock_get.return_value.json.side_effect = [
                    json_employees,
                    json_departments,
                ]
                resp = self.client.delete("/delete_employee/1", follow=True)
        self.assertTemplateUsed(resp, "employees/employees.html")
        self.assertIn(b"Successfully deleted Andrey Borsuk", resp.content)
