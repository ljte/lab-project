from unittest import mock

from django.test import Client, TestCase


resp_json = [
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
    }
]

class TestDepartmentViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_departments_page(self):
        with mock.patch("requests.get") as mock_req:
            mock_req.return_value.status_code = 200
            mock_req.return_value.json.return_value = resp_json
            resp = self.client.get("/departments/")
        self.assertTemplateUsed(resp, "departments/departments.html")
        self.assertIn(b"Marketing department", resp.content)

    def test_post_department(self):
        with mock.patch("requests.post") as mock_req:
            with mock.patch("requests.get") as mock_get:
                mock_req.return_value.status_code = 201
                mock_get.return_value.status_code = 200
                mock_get.return_value.json.return_value = resp_json[0]
                resp = self.client.post("/add_department/", resp_json[0], follow=True)
        self.assertTemplateUsed(resp, "departments/departments.html")
        self.assertIn(b"Successfully added Marketing department", resp.content)

    def test_put_department(self):
        with mock.patch("requests.put") as mock_req:
            with mock.patch("requests.get") as mock_get:
                mock_req.return_value.status_code = 204
                mock_get.return_value.status_code = 200
                mock_get.return_value.json.return_value = resp_json[0]
                resp = self.client.post("/edit_department/1", {"name": "Update department"}, follow=True)
        self.assertTemplateUsed(resp, "departments/departments.html")
        self.assertIn(b"Successfully edited Marketing department", resp.content)
