import unittest
from app.orders import get_order

class OrderTests(unittest.TestCase):
    def test_get_order(self):
        self.assertEqual(get_order(1).status, 'NEW')

    def test_unknown_order(self):
        with self.assertRaises(ValueError):
            get_order(999)

if __name__ == '__main__':
    unittest.main()
