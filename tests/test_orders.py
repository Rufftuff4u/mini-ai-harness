import unittest
from app.orders import ORDERS, Order, cancel_order, get_order

class OrderTests(unittest.TestCase):
    def test_get_order(self):
        self.assertEqual(get_order(1).status, 'NEW')

    def test_unknown_order(self):
        with self.assertRaises(ValueError):
            get_order(999)

    def test_cancel_new_order(self):
        order = Order(3)
        ORDERS[3] = order
        try:
            self.assertIs(cancel_order(3), order)
            self.assertEqual(order.status, 'CANCELLED')
        finally:
            del ORDERS[3]

    def test_cancel_shipped_order_rejected(self):
        with self.assertRaises(ValueError):
            cancel_order(2)
        self.assertEqual(get_order(2).status, 'SHIPPED')

    def test_cancelled_order_rejected(self):
        order = Order(4, 'CANCELLED')
        ORDERS[4] = order
        try:
            with self.assertRaises(ValueError):
                cancel_order(4)
            self.assertEqual(order.status, 'CANCELLED')
        finally:
            del ORDERS[4]

    def test_cancel_unknown_order_rejected(self):
        with self.assertRaises(ValueError):
            cancel_order(999)

if __name__ == '__main__':
    unittest.main()
