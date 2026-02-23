class HotelException(Exception):
    """Базовое исключение для всех ошибок системы отеля"""
    pass

class RoomNotAvailableError(HotelException):
    """Выбрасывается, если номер занят, не найден или находится на ремонте"""
    pass

class BookingInvalidStatusError(HotelException):
    """Выбрасывается при попытке выполнить действие, несовместимое со статусом бронирования"""
    pass

class GuestNotFoundError(HotelException):
    """Выбрасывается, если гость с таким ID не найден"""
    pass

class PaymentError(HotelException):
    """Выбрасывается при ошибках оплаты"""
    pass

class EntityNotFoundError(HotelException):
    """Универсальное исключение, если сущность (номер, бронь, сотрудник) не найдена"""
    pass