from abc import ABC, abstractmethod

class Coupon(ABC):
    @abstractmethod
    def apply(self, amount: float) -> float: 
        pass
    
    @abstractmethod
    def is_valid(self) -> bool:
        pass