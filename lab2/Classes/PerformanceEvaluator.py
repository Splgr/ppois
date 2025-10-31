from abc import ABC, abstractmethod
from Supplier import Supplier

class PerformanceEvaluator(ABC):
    @abstractmethod
    def evaluate(self, supplier: 'Supplier') -> bool: 
        pass