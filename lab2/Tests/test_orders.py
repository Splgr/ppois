import unittest
from datetime import datetime
from Order import Order
from Drug import Drug
from Customer import Customer
from exceptions import OrderCancellationError
from PercentageCoupon import PercentageCoupon
from FixedAmountCoupon import FixedAmountCoupon

class TestOrderUnit(unittest.TestCase):
    
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

    def test_order_expedite_priority(self):
        self.order.expedite()
        self.assertEqual(self.order.priority, "High")

    def test_order_normalize_priority(self):
        self.order.expedite()
        self.order.normalize_priority()
        self.assertEqual(self.order.priority, "Normal")

    def test_order_is_empty(self):
        self.assertTrue(self.order.is_empty())
        self.order.add_drug(self.drug)
        self.assertFalse(self.order.is_empty())

    def test_order_contains_drug(self):
        self.order.add_drug(self.drug)
        self.assertTrue(self.order.contains_drug(self.drug))

    def test_order_discount_amount_with_coupon(self):
        self.order.add_drug(self.drug)
        coupon = PercentageCoupon(10)
        self.order.apply_coupon(coupon)
        self.assertGreater(self.order.discount_amount, 0)

    def test_order_discount_amount_without_coupon(self):
        self.order.add_drug(self.drug)
        self.assertEqual(self.order.discount_amount, 0)

    def test_order_remove_customer_success(self):
        self.order.set_customer(self.customer)
        self.order.remove_customer()
        self.assertIsNone(self.order.customer)

    def test_order_recalculate_total_after_remove_drug(self):
        drug2 = Drug("Витамин C", "500mg", 50.0, "BATCH002", "room temp", "Витамин")
        self.order.add_drug(self.drug)
        self.order.add_drug(drug2)
        initial_total = self.order.total_amount
        self.order.remove_drug(drug2)
        self.assertLess(self.order.total_amount, initial_total)

    def test_order_mark_as_shipped_success(self):
        self.order.add_drug(self.drug)
        self.order.approve()
        self.order.mark_as_shipped()
        self.assertEqual(self.order.status, "Shipped")

    def test_order_cannot_mark_as_shipped_without_approval(self):
        self.order.add_drug(self.drug)
        with self.assertRaises(Exception) as context:
            self.order.mark_as_shipped()
        self.assertIn("Можно отгрузить только утверждённый заказ", str(context.exception))
        
class TestOrderCouponsUnit(unittest.TestCase):
    
    def setUp(self):
        self.order = Order("ORDER001", datetime.now())
        self.drug = Drug("Аспирин", "500mg", 100.0, "BATCH001", "room temp", "Обезболивающее")
        self.coupon = PercentageCoupon(10)  # 10% скидка

    def test_apply_coupon_success(self):
        self.order.add_drug(self.drug)
        initial_amount = self.order.total_amount

        self.order.apply_coupon(self.coupon)
  
        self.assertLess(self.order.total_amount, initial_amount)
        self.assertEqual(self.order.applied_coupon, self.coupon)

    def test_remove_coupon_success(self):
        self.order.add_drug(self.drug)
        initial_amount = self.order.total_amount
        self.order.apply_coupon(self.coupon)

        self.order.remove_coupon()
        
        self.assertEqual(self.order.total_amount, initial_amount)
        self.assertIsNone(self.order.applied_coupon)

    def test_apply_fixed_amount_coupon(self):
        self.order.add_drug(self.drug)
        coupon = FixedAmountCoupon(50.0)
        self.order.apply_coupon(coupon)
        self.assertIsNotNone(self.order.applied_coupon)

    def test_coupon_application_updates_total_amount(self):
        self.order.add_drug(self.drug)
        initial_total = self.order.total_amount
        self.order.apply_coupon(self.coupon)
        self.assertLess(self.order.total_amount, initial_total)