import unittest
from Customer import Customer
from OverTheCounterDrug import OverTheCounterDrug
from exceptions import InvalidDrugError
from datetime import timedelta

class TestCustomerUnit(unittest.TestCase):
    
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
        
class TestOverTheCounterDrugUnit(unittest.TestCase):
    """Unit тесты для OverTheCounterDrug"""
    
    def test_otc_extend_shelf_life_positive_days(self):
        # Arrange
        drug = OverTheCounterDrug("Витамин C", "500mg", 50.0, "BATCH003", "room temp", "Витамин")
        original_expiration = drug.expiration_date
        
        # Act
        drug.extend_shelf_life(30)
        
        # Assert
        self.assertEqual(drug.expiration_date, original_expiration + timedelta(days=30))

    def test_otc_extend_shelf_life_raises_error_on_negative_days(self):
        # Arrange
        drug = OverTheCounterDrug("Витамин C", "500mg", 50.0, "BATCH003", "room temp", "Витамин")
        
        # Act & Assert
        with self.assertRaises(InvalidDrugError) as context:
            drug.extend_shelf_life(-5)
        self.assertIn("Дни должны быть положительными", str(context.exception))

    def test_otc_recommend_alternative_same_category_different_name(self):
        # Arrange
        drug = OverTheCounterDrug("Витамин C", "500mg", 50.0, "BATCH003", "room temp", "Витамин")
        
        # Act
        result = drug.recommend_alternative("Витамин D", "Витамин")
        
        # Assert
        self.assertIn("Рекомендуем другие препараты категории 'Витамин'", result)

    def test_otc_recommend_alternative_same_name(self):
        # Arrange
        drug = OverTheCounterDrug("Витамин C", "500mg", 50.0, "BATCH003", "room temp", "Витамин")
        
        # Act
        result = drug.recommend_alternative("Витамин C", "Витамин")
        
        # Assert
        self.assertEqual(result, "Альтернативы не найдены")