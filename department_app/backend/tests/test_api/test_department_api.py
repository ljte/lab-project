from datetime import date

from django.http import Http404
from django.test import Client, TestCase

from backend.models import Department, Employee
from backend.service import get_all, get_obj, save_obj

API_URL = "/api/departments/"


class TestDepartmentApi(TestCase):
    def setUp(self):
        save_obj(Department(id=555, name="Marketing department"))
        save_obj(Department(id=666, name="Management department"))
        save_obj(Department(id=777, name="Delete department"))
        save_obj(
            Employee(
                id=555,
                fullname="Semen Borzov",
                salary=212.2,
                bday=date(1998, 12, 12),
                department=get_obj(Department, id=555),
            )
        )
        self.client = Client()

    def test_get_all(self):
        resp = self.client.get(API_URL)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 3)

    def test_get_with_id(self):
        resp = self.client.get(f"{API_URL}555")
        self.assertEqual(resp.json().get("name"), "Marketing department")
        self.assertEqual(resp.status_code, 200)

    def test_get_with_search_pattern(self):
        resp = self.client.get(f"{API_URL}", {"search_pattern": "Management"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)
        self.assertEqual(resp.json()[0].get("name"), "Management department")

    def test_filter_by_salary(self):
        query_dict = {"comparison_operator": ">", "salary": 123.3}
        resp = self.client.get(API_URL, query_dict)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.json(),
            [
                {
                    "id": 555,
                    "name": "Marketing department",
                    "number_of_employees": 1,
                    "average_salary": 212.2,
                }
            ],
        )

    def test_filter_by_salary_without_operator(self):
        query_dict = {"salary": 12312.32}
        resp = self.client.get(API_URL, query_dict)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 3)

    def test_filter_by_salary_without_salary(self):
        query_dict = {"comparison_operator": "<>"}
        resp = self.client.get(API_URL, query_dict)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json(), {"message": "Salary is empty"})

    def test_get_with_wrong_id(self):
        resp = self.client.get(f"{API_URL}21412412412412")
        self.assertEqual(resp.status_code, 404)
        resp = self.client.get(f"{API_URL}wrong_id")
        self.assertEqual(resp.status_code, 404)

    def test_post_with_valid_data(self):
        data = {"name": "Post department"}
        resp = self.client.post("/api/departments/", data)
        self.assertIn(
            get_obj(Department, name="Post department"),
            get_all(Department),
        )
        self.assertEqual(resp.status_code, 201)

    def test_post_with_invalid_data(self):
        data = {"name": "Post123132 department"}
        resp = self.client.post("/api/departments/", data)
        self.assertEqual(resp.status_code, 400)

        data = {"name": "Management department"}
        resp = self.client.post("/api/departments/", data)
        self.assertEqual(resp.status_code, 400)

    def test_put_with_valid_data(self):
        resp = self.client.put(f"{API_URL}555", "name=Put department")
        self.assertEqual(resp.status_code, 204)
        self.assertIn(get_obj(Department, name="Put department"), get_all(Department))
        with self.assertRaises(Http404):
            get_obj(Department, name="Marketing department")

    def test_put_with_invalid_data(self):
        resp = self.client.put(f"{API_URL}555", "name=Put1234 department")
        self.assertEqual(resp.status_code, 400)
        self.assertIn(
            get_obj(Department, name="Marketing department"),
            get_all(Department),
        )

    def test_delete(self):
        resp = self.client.delete(f"{API_URL}777")
        self.assertEqual(resp.json().get("name"), "Delete department")
        self.assertEqual(resp.status_code, 200)
        with self.assertRaises(Http404):
            get_obj(Department, name="Delete department")

    def test_delete_fails(self):
        resp = self.client.delete("/api/departments/1241212512512")
        self.assertEqual(resp.status_code, 404)
