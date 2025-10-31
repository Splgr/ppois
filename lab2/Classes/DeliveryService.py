from typing import List, Dict
from datetime import timedelta
from Order import Order

class DeliveryService:
    def __init__(self, service_name: str, delivery_fee: float, max_distance: int):
        self.service_name = service_name
        self.delivery_fee = delivery_fee
        self.max_distance = max_distance
        self._available_couriers: List[str] = []
        self._delivery_times: Dict[str, timedelta] = {}
        self._vehicle_types: List[str] = ["car", "bike", "walk"]

    def assign_courier(self, order: Order) -> str:
        return f"Курьер назначен для заказа {order.order_id}"