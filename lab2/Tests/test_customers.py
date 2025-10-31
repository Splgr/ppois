import unittest
from Customer import Customer

class TestCustomerUnit(unittest.TestCase):
    """Unit тесты для Customer"""
    
    def test_customer_creation(self):
        customer = Customer("Иван Иванов", "ул. Ленина 1", "ivan@mail.ru", "+79990001122", 5000.0)
        
        self.assertEqual(customer.name, "Иван Иванов")
        self.assertEqual(customer.address, "ул. Ленина 1")
        self.assertEqual(customer.email, "ivan@mail.ru")
        self.assertEqual(customer.phone, "+79990001122")
        self.assertEqual(customer.budget, 5000.0)

    def test_customer_attributes_types(self):
        customer = Customer("Иван Иванов", "ул. Ленина 1", "ivan@mail.ru", "+79990001122", 5000.0)
        
        self.assertIsInstance(customer.name, str)
        self.assertIsInstance(customer.address, str)
        self.assertIsInstance(customer.email, str)
        self.assertIsInstance(customer.phone, str)
        self.assertIsInstance(customer.budget, float)