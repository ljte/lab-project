from datetime import date

from backend.models import Department, Employee
from backend.service import get_all, get_obj, save_obj
from django.http import Http404
from django.test import Client, TestCase

API_URL = "/api/employees/"


class TestEmployeeApi(TestCase):
    def setUp(self):
        dep1 = Department(id=555, name="Marketing department")
        dep2 = Department(id=666, name="Management department")
        Department.objects.bulk_create([dep1, dep2])
        save_obj(
            Employee(
                id=555,
                fullname="Semen Borzov",
                salary=212.2,
                bday=date(1998, 12, 12),
                department=dep1,
            )
        )
        save_obj(
            Employee(
                id=666,
                fullname="Delete Employee",
                salary=555.5,
                bday=date(1965, 5, 23),
                department=dep2,
            )
        )
        self.client = Client()

    def test_get_all(self):
        resp = self.client.get(API_URL)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 2)

    def test_get_with_id(self):
        resp = self.client.get("/api/employees/555")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["fullname"], "Semen Borzov")

    def test_get_with_invalid_id(self):
        resp = self.client.get("/api/employees/123123")
        self.assertEqual(resp.status_code, 404)

    def test_post_with_valid_data(self):
        emp = {
            "fullname": "Anna Kolkova",
            "salary": 121.22,
            "bday": date(1983, 10, 23),
            "department": "Marketing department",
        }
        resp = self.client.post(API_URL, data=emp)
        self.assertEqual(resp.status_code, 201)
        self.assertIn(get_obj(Employee, fullname="Anna Kolkova"), get_all(Employee))

    def test_post_with_invalid_name(self):
        emp = {
            "fullname": "Anna12312 Kolkova",
            "salary": 121.22,
            "bday": date(1983, 10, 23),
            "department": "Marketing department",
        }
        resp = self.client.post(API_URL, data=emp)
        self.assertEqual(resp.status_code, 400)
        with self.assertRaises(Http404):
            get_obj(Employee, fullname="Anna12312 Kolkova")

    def test_post_with_invalid_bday(self):
        emp = {
            "fullname": "Anna Kolkova",
            "salary": 121.22,
            "bday": date(1234, 10, 23),
            "department": "Marketing department",
        }
        resp = self.client.post(API_URL, data=emp)
        self.assertEqual(resp.status_code, 400)
        with self.assertRaises(Http404):
            get_obj(Employee, fullname="Anna Kolkova")

    def test_put_with_valid_data(self):
        put_emp = "fullname=Maksim Borodko&salary=123&bday=1986-12-29"
        resp = self.client.put(f"{API_URL}555", put_emp)
        self.assertEqual(resp.status_code, 204)
        emp = get_obj(Employee, id=555)
        self.assertEqual(emp.fullname, "Maksim Borodko")
        self.assertEqual(emp.bday, date(1986, 12, 29))
        self.assertEqual(int(emp.salary), 123)
        with self.assertRaises(Http404):
            get_obj(Employee, fullname="Semen Borzov")

    def test_put_with_invalid_data(self):
        put_emp = "fullname=Semen12412 Borodko&salary=555"
        resp = self.client.put(f"{API_URL}555", put_emp)
        self.assertEqual(resp.status_code, 400)
        assert get_obj(Employee, fullname="Semen Borzov")

    def test_delete(self):
        resp = self.client.delete(f"{API_URL}666")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json().get("fullname"), "Delete Employee")
        with self.assertRaises(Http404):
            get_obj(Employee, id=666)

    def test_delete_fails(self):
        resp = self.client.delete(f"{API_URL}1241241")
        self.assertEqual(resp.status_code, 404)
