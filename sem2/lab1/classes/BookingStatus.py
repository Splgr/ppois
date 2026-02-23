class BookingStatus:
    CONFIRMED = "confirmed"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    CANCELLED = "cancelled"
    
    @staticmethod
    def display(status: str) -> str:
        mapping = {
            "confirmed": "Подтверждено",
            "checked_in": "Заселен",
            "checked_out": "Выселен",
            "cancelled": "Отменено"
        }
        return mapping.get(status, status)