from django.test import Client, TestCase

from ..models import Department
from ..service import save_obj


class TestDepartmentApi(TestCase):
    def setUp(self):
        save_obj(Department(name="Marketing department"))
        save_obj(Department(name="Management department"))
        self.client = Client()

    def test_get_all(self):
        resp = self.client.get("/api/departments/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 2)

    def test_get_with_id(self):
        save_obj(Department(id=500, name="Finance department"))
        resp = self.client.get("/api/departments/500")
        self.assertEqual(resp.json().get("name"), "Finance department")
        self.assertEqual(resp.status_code, 200)

    def test_get_with_wrong_id(self):
        resp = self.client.get("/api/departments/21412412412412")
        self.assertEqual(resp.status_code, 404)
        resp = self.client.get("/api/departments/asgdgasd")
        self.assertEqual(resp.status_code, 404)

    def test_post_with_valid_data(self):
        data = {"name": "Post department"}
        resp = self.client.post("/api/departments/", data)
        self.assertIn(
            Department.objects.filter(name="Post department").first(),
            Department.objects.all(),
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
        data = {"name": "Put department"}
        dep = Department.objects.filter(name="Marketing department").first()
        resp = self.client.put(
            "/api/departments/%d" % dep.id, data, content_type="application/json"
        )
        self.assertIn(
            Department.objects.filter(name="Put department").first(),
            Department.objects.all(),
        )
        self.assertEqual(
            list(Department.objects.filter(name="Marketing department").all()), []
        )
        self.assertEqual(resp.status_code, 204)

    def test_put_with_invalid_data(self):
        dep = Department.objects.filter(name="Marketing department").first()
        resp = self.client.put(
            "/api/departments/%d" % dep.id, "name=Put1234 department"
        )
        self.assertNotIn(Department(name="Put department"), Department.objects.all())
        self.assertIn(
            Department.objects.filter(name="Marketing department").first(),
            Department.objects.all(),
        )
        self.assertEqual(resp.status_code, 400)

    def test_delete(self):
        dep = Department.objects.create(name="Delete department")
        resp = self.client.delete(f"/api/departments/{dep.id}")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            list(Department.objects.filter(name="Delete department").all()), []
        )

    def test_delete_fails(self):
        resp = self.client.delete("/api/departments/1241212512512")
        self.assertEqual(resp.status_code, 404)
