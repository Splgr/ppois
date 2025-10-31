from Coupon import Coupon

class NoCoupon(Coupon):
    def apply(self, amount: float) -> float:
        return amount
    
    def is_valid(self) -> bool:
        return True