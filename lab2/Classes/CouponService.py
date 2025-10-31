from datetime import datetime, timedelta
from Coupon import Coupon
from PercentageCoupon import PercentageCoupon
from FixedAmountCoupon import FixedAmountCoupon

class CouponService:
    @staticmethod
    def validate_and_apply(coupon: Coupon, order_amount: float) -> float:
        if not coupon.is_valid():
            raise Exception("Купон недействителен")
        
        if isinstance(coupon, FixedAmountCoupon) and order_amount < coupon.min_order_amount:
            raise Exception(f"Минимальная сумма заказа: {coupon.min_order_amount}")
            
        return coupon.apply(order_amount)
    
    @staticmethod
    def create_percentage_coupon(discount_percent: float, days_valid: int = 30) -> PercentageCoupon:
        expiry_date = datetime.now() + timedelta(days=days_valid)
        return PercentageCoupon(discount_percent, expiry_date)
    
    @staticmethod
    def create_fixed_coupon(discount_amount: float, min_order_amount: float = 0, days_valid: int = 30) -> FixedAmountCoupon:
        expiry_date = datetime.now() + timedelta(days=days_valid)
        return FixedAmountCoupon(discount_amount, min_order_amount, expiry_date)