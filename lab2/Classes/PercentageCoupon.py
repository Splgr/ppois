from datetime import datetime
from Coupon import Coupon

class PercentageCoupon(Coupon):
    def __init__(self, discount_percent: float, expiry_date: datetime = None):
        if not 0 < discount_percent <= 100:
            raise Exception("Процент скидки должен быть от 0 до 100")
        self.discount_percent = discount_percent
        self.expiry_date = expiry_date
    
    def apply(self, amount: float) -> float:
        return amount * (1 - self.discount_percent / 100)
    
    def is_valid(self) -> bool:
        if self.expiry_date and datetime.now() > self.expiry_date:
            return False
        return True