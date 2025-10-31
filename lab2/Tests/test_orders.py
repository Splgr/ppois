import unittest
from datetime import datetime
from Order import Order
from Drug import Drug
from Customer import Customer
from exceptions import OrderCancellationError

class TestOrderUnit(unittest.TestCase):
    """Unit тесты для Order"""
    
    def setUp(self):
        self.order = Order("ORDER001", datetime.now())
        self.drug = Drug("Аспирин", "500mg", 100.0, "BATCH001", "room temp", "Обезболивающее")
        self.customer = Customer("Иван Иванов", "ул. Ленина 1", "ivan@mail.ru", "+79990001122", 5000.0)

    def test_order_creation(self):
        self.assertEqual(self.order.order_id, "ORDER001")
        self.assertEqual(self.order.status, "Pending")
        self.assertEqual(self.order.total_amount, 0.0)

    def test_set_customer(self):
        self.order.set_customer(self.customer)
        self.assertEqual(self.order.customer.name, "Иван Иванов")

    def test_add_drug(self):
        self.order.add_drug(self.drug)
        self.assertEqual(self.order.total_amount, 300.0)  # 100 + 200 доставка
        self.assertEqual(self.order.get_drug_count(), 1)

    def test_remove_drug(self):
        self.order.add_drug(self.drug)
        self.order.remove_drug(self.drug)
        self.assertEqual(self.order.get_drug_count(), 0)
        self.assertEqual(self.order.status, "Cancelled")

    def test_approve_order(self):
        self.order.add_drug(self.drug)
        self.order.approve()
        self.assertEqual(self.order.status, "Approved")

    def test_cancel_order(self):
        self.order.cancel()
        self.assertEqual(self.order.status, "Cancelled")

    def test_cannot_add_drug_to_shipped_order(self):
        self.order.add_drug(self.drug)
        self.order.approve()
        self.order.mark_as_shipped()
        
        new_drug = Drug("Витамин C", "500mg", 50.0, "BATCH002", "room temp", "Витамин")
        with self.assertRaises(OrderCancellationError) as context:
            self.order.add_drug(new_drug)
        self.assertIn("Нельзя менять завершённый заказ", str(context.exception))