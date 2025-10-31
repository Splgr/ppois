from typing import List
from Drug import Drug
from exceptions import WarehouseCapacityExceededError, InsufficientStockError

class Stock:
    def __init__(self, stock_id: str, location: str, capacity: int):
        self.stock_id = stock_id
        self.location = location
        self.capacity = capacity
        self._quantity = 0
        self._drugs: List[Drug] = []

    @property
    def quantity(self) -> int:
        return self._quantity

    def add_drugs(self, drugs: List[Drug]) -> None:
        """Добавить лекарства на склад"""
        if self._quantity + len(drugs) > self.capacity:
            raise WarehouseCapacityExceededError(
                f"Превышена вместимость склада. Свободно: {self.capacity - self._quantity}"
            )
        
        self._drugs.extend(drugs)
        self._quantity += len(drugs)

    def remove_drugs(self, count: int) -> List[Drug]:
        """Изъять лекарства со склада"""
        if count > self._quantity:
            raise InsufficientStockError(
                f"Недостаточно на складе. Доступно: {self._quantity}, запрошено: {count}"
            )
        
        removed_drugs = self._drugs[:count]
        self._drugs = self._drugs[count:]
        self._quantity -= count
        return removed_drugs

    def get_utilization_percentage(self) -> float:
        """Процент заполнения склада"""
        return (self._quantity / self.capacity) * 100