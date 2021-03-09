from datetime import date

from django.test import Client, TestCase

from ..models import Department, Employee
from ..service import save_obj


class TestEmployeeApi(TestCase):
    def setUp(self):
        dep1 = Department(name="Marketing department")
        dep2 = Department(name="Management department")
        Department.objects.bulk_create([dep1, dep2])
        emp1 = Employee(
            first_name="Andrey",
            second_name="Semenov",
            salary=212.2,
            bday=date(1998, 12, 12),
            department=dep1,
        )
        save_obj(emp1)
        self.client = Client()

    def test_get_all_works_fine(self):
        resp = self.client.get("/api/employees/")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)

    def test_get_with_id(self):
        save_obj(
            Employee(
                id=500,
                first_name="Vasiliy",
                second_name="Borko",
                bday=date(1988, 5, 23),
                salary=1412.3,
                department=Department.objects.first(),
            )
        )
        resp = self.client.get("/api/employees/500")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["first_name"], "Vasiliy")

    def test_post_with_valid_data(self):
        emp = {
            "first_name": "Anna",
            "second_name": "Kolkova",
            "salary": 121.22,
            "bday": date(1983, 10, 23),
            "department": Department.objects.first(),
        }
        resp = self.client.post("/api/employees/", data=emp)

        self.assertEqual(resp.status_code, 201)
        self.assertIn(
            Employee.objects.filter(first_name="Anna").first(), Employee.objects.all()
        )

    def test_post_with_invalid_name(self):
        emp = {
            "first_name": "Anna12312",
            "second_name": "Kolkova",
            "salary": 121.22,
            "bday": date(1983, 10, 23),
            "department": Department.objects.first(),
        }
        resp = self.client.post("/api/employees/", data=emp)

        emp = Employee(**emp)

        self.assertEqual(resp.status_code, 400)
        self.assertNotIn(emp, Employee.objects.all())

    def test_post_with_invalid_bday(self):
        emp = {
            "first_name": "Anna",
            "second_name": "Kolkova",
            "salary": 121.22,
            "bday": date(1234, 10, 23),
            "department": Department.objects.first(),
        }
        resp = self.client.post("/api/employees/", data=emp)

        emp = Employee(**emp)

        self.assertEqual(resp.status_code, 400)
        self.assertNotIn(emp, Employee.objects.all())

    def test_put_with_valid_data(self):
        emp = {
            "first_name": "Andrey",
            "second_name": "Borzunov",
            "salary": 121.22,
            "bday": date(1983, 10, 23),
            "department": Department.objects.first(),
        }
        self.client.post("/api/employees/", data=emp)
        put_emp = {"first_name": "Semen", "salary": 555}
        emp = Employee.objects.filter(second_name="Borzunov").first()
        resp = self.client.put(
            f"/api/employees/{emp.id}", data=put_emp, content_type="application/json"
        )

        emp = Employee.objects.filter(second_name="Borzunov").first()
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(emp.first_name, "Semen")
        self.assertEqual(int(emp.salary), 555)

    def test_put_with_invalid_data(self):
        emp = {
            "first_name": "Andrey",
            "second_name": "Borzunov",
            "salary": 121.22,
            "bday": date(1983, 10, 23),
            "department": Department.objects.first(),
        }
        self.client.post("/api/employees/", data=emp)
        put_emp = {"first_name": "Semen12412", "salary": 555}
        emp = Employee.objects.filter(second_name="Borzunov").first()
        resp = self.client.put(
            f"/api/employees/{emp.id}", data=put_emp, content_type="application/json"
        )

        emp = Employee.objects.filter(second_name="Borzunov").first()
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(emp.first_name, "Andrey")
        self.assertEqual(int(emp.salary), 121)

    def test_delete(self):
        emp = {
            "first_name": "Gleb",
            "second_name": "Borzunov",
            "salary": 121.22,
            "bday": date(1983, 10, 23),
            "department": Department.objects.first(),
        }
        self.client.post("/api/employees/", data=emp)

        emp = Employee.objects.filter(second_name="Borzunov").first()
        resp = self.client.delete(f"/api/employees/{emp.id}")

        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(emp, Employee.objects.all())

    def test_delete_fails(self):
        resp = self.client.delete("/api/employees/124124124124")

        self.assertEqual(resp.status_code, 404)
