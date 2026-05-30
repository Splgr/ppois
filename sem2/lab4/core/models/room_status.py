class RoomStatus:
    AVAILABLE = "available"
    BOOKED = "booked"
    OCCUPIED = "occupied"
    MAINTENANCE = "maintenance"
    
    @staticmethod
    def display(status: str) -> str:
        mapping = {
            "available": "Свободен",
            "booked": "Забронирован",
            "occupied": "Заселен",
            "maintenance": "На ремонте"
        }
        return mapping.get(status, status)