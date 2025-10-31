from datetime import datetime
from Coupon import Coupon

class FixedAmountCoupon(Coupon):
    def __init__(self, discount_amount: float, min_order_amount: float = 0, expiry_date: datetime = None):
        if discount_amount <= 0:
            raise Exception("Сумма скидки должна быть положительной")
        self.discount_amount = discount_amount
        self.min_order_amount = min_order_amount
        self.expiry_date = expiry_date
    
    def apply(self, amount: float) -> float:
        new_amount = amount - self.discount_amount
        return max(new_amount, 0)
    
    def is_valid(self) -> bool:
        if self.expiry_date and datetime.now() > self.expiry_date:
            return False
        return True