from PerformanceEvaluator import PerformanceEvaluator
from Supplier import Supplier

class DefaultPerformanceEvaluator(PerformanceEvaluator):
    def evaluate(self, supplier: Supplier) -> bool:
        return supplier.rating > 4