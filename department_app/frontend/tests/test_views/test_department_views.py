from django.test import Client, TestCase


class TestDepartmentViews(TestCase):
    def setUp(self):
        self.client = Client()
