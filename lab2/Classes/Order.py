from datetime import datetime
from typing import List, Optional
from Drug import Drug
from Customer import Customer
from exceptions import OrderCancellationError, InsufficientStockError

class Order:
    def __init__(
        self,
        order_id: str,
        order_date: datetime,
        priority: str = "Normal"
    ):
        self.order_id = order_id
        self.order_date = order_date
        self.priority = priority
        self._customer = None
        self._drugs: List[Drug] = []
        self._status = "Pending"
        self._total_amount = 0.0
        self._applied_coupon = None
        self._shipping_cost = 200.0

    @property
    def total_amount(self) -> float:
        return self._total_amount

    @property
    def status(self) -> str:
        return self._status

    @property
    def customer(self):
        return self._customer

    @property
    def drugs(self) -> List[Drug]:
        return self._drugs.copy()

    @property
    def applied_coupon(self):
        return self._applied_coupon

    @property
    def discount_amount(self) -> float:
        base_amount = sum(drug.price for drug in self._drugs)
        if self._applied_coupon is None:
            return 0.0
        return base_amount - self._applied_coupon.apply(base_amount)

    def set_customer(self, customer: Customer) -> None:
        if self._customer:
            raise Exception("Клиент уже назначен")
        self._customer = customer

    def remove_customer(self) -> None:
        if self._status != "Pending":
            raise Exception("Нельзя удалить клиента из активного заказа")
        self._customer = None

    def add_drug(self, drug: Drug) -> None:
        if self._status in ["Shipped", "Cancelled"]:
            raise OrderCancellationError("Нельзя менять завершённый заказ")
        
        self._drugs.append(drug)
        self._recalculate_total()

    def remove_drug(self, drug: Drug) -> None:
        if self._status in ["Shipped", "Cancelled"]:
            raise OrderCancellationError("Нельзя менять завершённый заказ")
        if drug not in self._drugs:
            raise Exception("Лекарство не в заказе")
            
        self._drugs.remove(drug)
        self._recalculate_total()
        
        if not self._drugs:
            self._status = "Cancelled"

    def _recalculate_total(self) -> None:
        base_amount = sum(drug.price for drug in self._drugs)
        
        if self._applied_coupon is None:
            discounted_amount = base_amount
        else:
            try:
                discounted_amount = self._applied_coupon.apply(base_amount)
            except Exception:
                self._applied_coupon = None
                discounted_amount = base_amount
        
        self._total_amount = discounted_amount + self._shipping_cost

    def apply_coupon(self, coupon) -> None:
        if self._status != "Pending":
            raise Exception("Купон можно применить только к ожидающему заказу")
        
        base_amount = sum(drug.price for drug in self._drugs)
        
        try:
            discounted_amount = coupon.apply(base_amount)
            self._applied_coupon = coupon
            self._recalculate_total()
        except Exception as e:
            raise Exception(f"Не удалось применить купон: {e}")

    def remove_coupon(self) -> None:
        if self._status != "Pending":
            raise Exception("Купон можно удалить только из ожидающего заказа")
        self._applied_coupon = None
        self._recalculate_total()

    def approve(self) -> None:
        if self._status != "Pending":
            raise Exception("Можно утвердить только ожидающий заказ")
        if not self._drugs:
            raise Exception("Нельзя утвердить пустой заказ")
            
        self._status = "Approved"

    def cancel(self) -> None:
        if self._status == "Shipped":
            raise Exception("Нельзя отменить отгруженный заказ")
        self._status = "Cancelled"

    def mark_as_shipped(self) -> None:
        if self._status != "Approved":
            raise Exception("Можно отгрузить только утверждённый заказ")
        self._status = "Shipped"

    def expedite(self) -> None:
        if self._status != "Pending":
            raise Exception("Можно ускорить только ожидающий заказ")
        self.priority = "High"

    def normalize_priority(self) -> None:
        self.priority = "Normal"

    def is_empty(self) -> bool:
        return len(self._drugs) == 0

    def contains_drug(self, drug: Drug) -> bool:
        return drug in self._drugs

    def get_drug_count(self) -> int:
        return len(self._drugs)

    def __str__(self) -> str:
        customer_name = self._customer.name if self._customer else "Не назначен"
        coupon_info = f", купон: {type(self._applied_coupon).__name__}" if self._applied_coupon else ""
        discount_info = f", скидка: {self.discount_amount}₽" if self.discount_amount > 0 else ""
        
        return (f"Заказ {self.order_id}: {self.total_amount}₽"
                f"{discount_info}, статус: {self.status}{coupon_info}, "
                f"клиент: {customer_name}, лекарств: {len(self._drugs)}")