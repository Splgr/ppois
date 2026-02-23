from RoomStatus import RoomStatus
from exceptions import RoomNotAvailableError
from exceptions import BookingInvalidStatusError

class Room:
    """Номер отеля"""
    def __init__(self, number: str, berths: int, price_per_day: float, room_type: str = "стандарт"):
        self.number = number
        self.berths = berths
        self.price_per_day = price_per_day
        self.room_type = room_type
        self.status = RoomStatus.AVAILABLE
        self.current_booking_id: str | None = None
    
    def assign_booking(self, booking_id: str):
        if self.status != RoomStatus.AVAILABLE:
            # Используем наше кастомное исключение
            raise RoomNotAvailableError(f"Номер {self.number} недоступен для бронирования (статус: {self.status})")
        self.status = RoomStatus.BOOKED
        self.current_booking_id = booking_id
    
    def occupy(self):
        if self.status != RoomStatus.BOOKED:
            # Используем наше кастомное исключение
            raise BookingInvalidStatusError(f"Номер {self.number} не был забронирован, нельзя заселить напрямую")
        self.status = RoomStatus.OCCUPIED
    
    def release(self):
        self.status = RoomStatus.AVAILABLE
        self.current_booking_id = None
    
    def to_dict(self) -> dict:
        return {
            "number": self.number,
            "berths": self.berths,
            "price_per_day": self.price_per_day,
            "room_type": self.room_type,
            "status": self.status,
            "current_booking_id": self.current_booking_id
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Room':
        room = Room(
            number=data["number"],
            berths=data["berths"],
            price_per_day=data["price_per_day"],
            room_type=data["room_type"]
        )
        room.status = data["status"]
        room.current_booking_id = data.get("current_booking_id")
        return room
    
    def __str__(self):
        return (f"Номер {self.number} ({self.room_type}, {self.berths} мест) - "
                f"{RoomStatus.display(self.status)}, {self.price_per_day:.2f} BYN/сутки")