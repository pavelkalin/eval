from django.test import TestCase


# Create your tests here.
class DemoTest(TestCase):
    def test_addition(self):
        self.assertEquals(2 + 2, 4)
