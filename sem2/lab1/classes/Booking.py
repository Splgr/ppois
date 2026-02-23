from BookingStatus import BookingStatus
from Guest import Guest
from Room import Room
from Period import Period
from ServiceOrder import ServiceOrder
from exceptions import BookingInvalidStatusError
from exceptions import PaymentError


class Booking:
    """Бронирование номера"""
    def __init__(self, booking_id: str, guest: Guest, room: Room, period: Period):
        self.id = booking_id
        self.guest = guest
        self.room = room
        self.period = period
        self.status = BookingStatus.CONFIRMED
        self.service_orders: list[ServiceOrder] = []
        self.total_paid = 0.0
    
    @property
    def total_amount(self) -> float:
        room_cost = self.room.price_per_day * self.period.duration_days
        services_cost = sum(order.price for order in self.service_orders)
        return room_cost + services_cost
    
    def check_in(self):
        if self.status != BookingStatus.CONFIRMED:
            # Используем наше кастомное исключение
            raise BookingInvalidStatusError("Невозможно выполнить регистрацию: бронирование не в статусе 'Подтверждено'")
        self.room.occupy()
        self.status = BookingStatus.CHECKED_IN
    
    def add_service(self, order: ServiceOrder):
        if self.status != BookingStatus.CHECKED_IN:
            # Используем наше кастомное исключение
            raise BookingInvalidStatusError("Услуги можно заказывать только после заселения (статус CHECKED_IN)")
        self.service_orders.append(order)
    
    def check_out(self, payment_amount: float):
        if self.status != BookingStatus.CHECKED_IN:
            raise BookingInvalidStatusError("Невозможно выселить: гость не заселен")
        if payment_amount < self.total_amount:
            # Используем наше кастомное исключение
            raise PaymentError(f"Недостаточная оплата. Требуется: {self.total_amount:.2f} BYN, внесено: {payment_amount:.2f} BYN")
        
        self.room.release()
        self.status = BookingStatus.CHECKED_OUT
        self.total_paid = payment_amount
    
    def to_dict(self) -> dict:
        return {
            "booking_id": self.id,
            "guest_id": self.guest.id,
            "room_number": self.room.number,
            "period": self.period.to_dict(),
            "status": self.status,
            "service_orders": [order.to_dict() for order in self.service_orders],
            "total_paid": self.total_paid
        }
    
    @staticmethod
    def from_dict(data: dict, guest: Guest, room: Room) -> 'Booking':
        booking = Booking(
            booking_id=data["booking_id"],
            guest=guest,
            room=room,
            period=Period.from_dict(data["period"])
        )
        booking.status = data["status"]
        booking.service_orders = [ServiceOrder.from_dict(o) for o in data.get("service_orders", [])]
        booking.total_paid = data.get("total_paid", 0.0)
        return booking
    
    def __str__(self):
        room_cost = self.room.price_per_day * self.period.duration_days
        services_cost = sum(o.price for o in self.service_orders)
        return (f"Бронь #{self.id} | {self.guest.name} | Номер {self.room.number} | "
                f"{self.period.start.strftime('%d.%m')} - {self.period.end.strftime('%d.%m')} | "
                f"Статус: {BookingStatus.display(self.status)}\n"
                f"  Стоимость: номер {room_cost:.2f} + услуги {services_cost:.2f} = {self.total_amount:.2f} BYN")