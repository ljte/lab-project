from django.test import TestCase

from backend.serializers.helpers import check_for_digits


class TestHelpers(TestCase):
    def test_check_for_digits_passes(self):
        self.assertFalse(check_for_digits("Dima Andreyko"))
        self.assertFalse(check_for_digits("Marketing department"))

    def test_check_for_digits_fails(self):
        self.assertTrue(check_for_digits("Dima31231 Andreyko"))
        self.assertTrue(check_for_digits("Marketing123123 department"))
