from datetime import datetime
from ServiceType import ServiceType

class ServiceOrder:
    """Заказ дополнительной услуги"""
    def __init__(self, order_id: str, guest_id: str, service_type: str, description: str, price: float):
        self.order_id = order_id
        self.guest_id = guest_id
        self.service_type = service_type
        self.description = description
        self.price = price
        self.ordered_at = datetime.now()
    
    def to_dict(self) -> dict:
        return {
            "order_id": self.order_id,
            "guest_id": self.guest_id,
            "service_type": self.service_type,
            "description": self.description,
            "price": self.price,
            "ordered_at": self.ordered_at.isoformat()
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'ServiceOrder':
        order = ServiceOrder(
            order_id=data["order_id"],
            guest_id=data["guest_id"],
            service_type=data["service_type"],
            description=data["description"],
            price=data["price"]
        )
        order.ordered_at = datetime.fromisoformat(data["ordered_at"])
        return order
    
    def __str__(self):
        return (f"[{self.ordered_at.strftime('%d.%m %H:%M')}] {ServiceType.display(self.service_type)}: "
                f"{self.description} - {self.price:.2f} BYN")
