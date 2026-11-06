import unittest
from metrics import total

class TotalTests(unittest.TestCase):
    def test_values(self):
        self.assertEqual(total([1, 2, 3]), 6)

    def test_empty(self):
        self.assertEqual(total([]), 0)
