from django.test import TestCase


# Create your tests here.
class DemoTest(TestCase):
    def test_addition(self):
        self.assertEquals(2 + 2, 4)

    def test_substraction(self):
        self.assertEquals(3 - 2, 1)

    def test_mupltiplication(self):
        self.assertEquals(2 * 2, 4)
