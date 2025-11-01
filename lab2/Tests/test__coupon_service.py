import unittest
from datetime import datetime, timedelta
from CouponService import CouponService
from PercentageCoupon import PercentageCoupon
from FixedAmountCoupon import FixedAmountCoupon
class TestCouponServiceUnit(unittest.TestCase):
    
    def setUp(self):
        self.coupon_service = CouponService()
    
    def test_validate_and_apply_percentage_coupon_success(self):
        # Arrange
        coupon = PercentageCoupon(20)  # 20% скидка
        order_amount = 100.0
        
        # Act
        result = self.coupon_service.validate_and_apply(coupon, order_amount)
        
        # Assert
        self.assertEqual(result, 80.0)  # 100 - 20%
    
    def test_validate_and_apply_fixed_coupon_success(self):
        # Arrange
        coupon = FixedAmountCoupon(30.0, min_order_amount=50.0)  # 30 руб скидка
        order_amount = 100.0
        
        # Act
        result = self.coupon_service.validate_and_apply(coupon, order_amount)
        
        # Assert
        self.assertEqual(result, 70.0)  # 100 - 30
    
    def test_validate_and_apply_expired_coupon_raises_error(self):
        # Arrange
        expiry_date = datetime.now() - timedelta(days=1)  # просроченный купон
        coupon = PercentageCoupon(10, expiry_date)
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            self.coupon_service.validate_and_apply(coupon, 100.0)
        self.assertIn("Купон недействителен", str(context.exception))
    
    def test_validate_and_apply_fixed_coupon_below_min_amount_raises_error(self):
        # Arrange
        coupon = FixedAmountCoupon(30.0, min_order_amount=100.0)
        order_amount = 50.0  # меньше минимальной суммы
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            self.coupon_service.validate_and_apply(coupon, order_amount)
        self.assertIn("Минимальная сумма заказа: 100.0", str(context.exception))
    
    def test_create_percentage_coupon(self):
        # Act
        coupon = self.coupon_service.create_percentage_coupon(15.0, days_valid=60)
        
        # Assert
        self.assertIsInstance(coupon, PercentageCoupon)
        self.assertEqual(coupon.discount_percent, 15.0)
        self.assertTrue(coupon.is_valid())
    
    def test_create_fixed_coupon(self):
        # Act
        coupon = self.coupon_service.create_fixed_coupon(
            discount_amount=50.0, 
            min_order_amount=200.0, 
            days_valid=45
        )
        
        # Assert
        self.assertIsInstance(coupon, FixedAmountCoupon)
        self.assertEqual(coupon.discount_amount, 50.0)
        self.assertEqual(coupon.min_order_amount, 200.0)
        self.assertTrue(coupon.is_valid())
    
    def test_create_fixed_coupon_default_values(self):
        # Act
        coupon = self.coupon_service.create_fixed_coupon(25.0)
        
        # Assert
        self.assertEqual(coupon.discount_amount, 25.0)
        self.assertEqual(coupon.min_order_amount, 0)  # значение по умолчанию
        self.assertTrue(coupon.is_valid())
    
    def test_coupon_integration_workflow(self):
        # Arrange & Act - создаем купон через сервис
        coupon = self.coupon_service.create_percentage_coupon(25.0, days_valid=30)
        
        # Assert - проверяем что он работает
        result = self.coupon_service.validate_and_apply(coupon, 200.0)
        self.assertEqual(result, 150.0)  # 200 - 25%
    
    def test_multiple_coupon_creations(self):
        # Act
        percentage_coupon = self.coupon_service.create_percentage_coupon(10.0)
        fixed_coupon = self.coupon_service.create_fixed_coupon(15.0, 50.0)
        
        # Assert
        self.assertIsInstance(percentage_coupon, PercentageCoupon)
        self.assertIsInstance(fixed_coupon, FixedAmountCoupon)
        
        # Проверяем применение обоих купонов
        result1 = self.coupon_service.validate_and_apply(percentage_coupon, 100.0)
        result2 = self.coupon_service.validate_and_apply(fixed_coupon, 100.0)
        
        self.assertEqual(result1, 90.0)  # 100 - 10%
        self.assertEqual(result2, 85.0)  # 100 - 15