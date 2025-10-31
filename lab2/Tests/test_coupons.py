import unittest
from datetime import datetime, timedelta
from PercentageCoupon import PercentageCoupon
from FixedAmountCoupon import FixedAmountCoupon
from Order import Order
from Drug import Drug

class TestPercentageCouponUnit(unittest.TestCase):
    def test_is_valid_when_no_expiry(self):
        coupon = PercentageCoupon(10)
        self.assertTrue(coupon.is_valid())

    def test_apply_discount(self):
        coupon = PercentageCoupon(10)
        result = coupon.apply(100.0)
        self.assertEqual(result, 90.0)

class TestFixedAmountCouponUnit(unittest.TestCase):
    def test_is_valid_when_no_expiry(self):
        coupon = FixedAmountCoupon(50.0)
        self.assertTrue(coupon.is_valid())

    def test_apply_discount_above_min_amount(self):
        coupon = FixedAmountCoupon(50.0, min_order_amount=100.0)
        result = coupon.apply(150.0)
        self.assertEqual(result, 100.0)

    def test_apply_discount_below_min_amount(self):
        coupon = FixedAmountCoupon(50.0, min_order_amount=100.0)
        result = coupon.apply(80.0)
        self.assertEqual(result, 30.0)

class TestOrderCouponsUnit(unittest.TestCase):
    def setUp(self):
        self.order = Order("ORDER001", datetime.now())
        self.drug = Drug("Аспирин", "500mg", 100.0, "BATCH001", "room temp", "Обезболивающее")

    def test_apply_percentage_coupon(self):
        self.order.add_drug(self.drug)
        coupon = PercentageCoupon(10)
        self.order.apply_coupon(coupon)
        self.assertIsNotNone(self.order.applied_coupon)

    def test_apply_fixed_amount_coupon(self):
        self.order.add_drug(self.drug)
        coupon = FixedAmountCoupon(50.0)
        self.order.apply_coupon(coupon)
        self.assertIsNotNone(self.order.applied_coupon)

    def test_remove_coupon(self):
        self.order.add_drug(self.drug)
        coupon = PercentageCoupon(10)
        self.order.apply_coupon(coupon)
        self.order.remove_coupon()
        self.assertIsNone(self.order.applied_coupon)