# core/reception.py
from datetime import datetime

from .models import Room, Guest, Booking, Period, ServiceOrder
from .storage import HotelStorage
from .exceptions import (
    GuestNotFoundError, 
    EntityNotFoundError, 
    RoomNotAvailableError,
    BookingInvalidStatusError
)

class Reception:
    """Фасад для операций ресепшена"""
    
    def __init__(self, storage: HotelStorage):
        self.storage = storage
    
    # Операция бронирования номера
    def book_room(self, guest_id: str, room_number: str, check_in: datetime, check_out: datetime) -> Booking:
        guest = self.storage.get_guest(guest_id)
        if not guest:
            raise GuestNotFoundError(f"Гость с ID {guest_id} не найден")
        
        room = self.storage.get_room(room_number)
        if not room:
            raise EntityNotFoundError(f"Номер {room_number} не найден в базе")
  
        try:
            period = Period(check_in, check_out)
            booking = self.storage.create_booking(guest, room, period)
            room.assign_booking(booking.id)
            self.storage.save_to_file()
            return booking
        except RoomNotAvailableError:
            raise
        
    def remove_service(self, booking_id: str, order_id: str):
        """Удалить дополнительную услугу из бронирования"""
        booking = self.storage.get_booking(booking_id)
        if not booking:
            raise EntityNotFoundError(f"Бронирование {booking_id} не найдено")
        
        if booking.status != "checked_in":
            raise BookingInvalidStatusError("Удалять услуги можно только у заселённых гостей")
        
        for i, order in enumerate(booking.service_orders):
            if order.order_id == order_id:
                del booking.service_orders[i]
                self.storage.save_to_file()
                return True
        
        raise EntityNotFoundError(f"Услуга {order_id} не найдена в брони {booking_id}")
    # Операция регистрации гостей
    def check_in_guest(self, booking_id: str):
        booking = self.storage.get_booking(booking_id)
        if not booking:
            raise EntityNotFoundError(f"Бронирование {booking_id} не найдено")
        booking.check_in() 
        self.storage.save_to_file()
    
    # Операция предоставления дополнительных услуг
    def order_service(self, booking_id: str, service_type: str, description: str, price: float) -> ServiceOrder:
        booking = self.storage.get_booking(booking_id)
        if not booking:
            raise EntityNotFoundError(f"Бронирование {booking_id} не найдено")
        
        # Здесь вылетит BookingInvalidStatusError если статус не CHECKED_IN
        order = self.storage.create_service_order(booking.guest.id, service_type, description, price)
        booking.add_service(order)
        self.storage.save_to_file()
        return order
    
    # Операция выселения и оплаты
    def check_out_guest(self, booking_id: str, payment_amount: float) -> float:
        booking = self.storage.get_booking(booking_id)
        if not booking:
            raise EntityNotFoundError(f"Бронирование {booking_id} не найдено")
        
        booking.check_out(payment_amount) # Может вылететь PaymentError или BookingInvalidStatusError
        self.storage.save_to_file()
        change = payment_amount - booking.total_amount
        return max(0.0, change)
    
    # Вспомогательные методы
    def get_all_rooms(self) -> list[Room]:
        return self.storage.get_all_rooms()
    
    def get_active_bookings(self) -> list[Booking]:
        return self.storage.get_active_bookings()
    
    def register_new_guest(self, name: str, contact: str) -> Guest:
        return self.storage.register_guest(name, contact)
    
    def save_data(self):
        self.storage.save_to_file()

