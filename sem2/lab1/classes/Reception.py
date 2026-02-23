from HotelStorage import HotelStorage
from datetime import datetime
from Booking import Booking
from exceptions import GuestNotFoundError
from exceptions import EntityNotFoundError
from Period import Period
from exceptions import RoomNotAvailableError
from ServiceOrder import ServiceOrder
from Room import Room
from Guest import Guest

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
            return booking
        except RoomNotAvailableError:
            raise
    
    # Операция регистрации гостей
    def check_in_guest(self, booking_id: str):
        booking = self.storage.get_booking(booking_id)
        if not booking:
            raise EntityNotFoundError(f"Бронирование {booking_id} не найдено")
        booking.check_in() # Может вылететь BookingInvalidStatusError
    
    # Операция предоставления дополнительных услуг
    def order_service(self, booking_id: str, service_type: str, description: str, price: float) -> ServiceOrder:
        booking = self.storage.get_booking(booking_id)
        if not booking:
            raise EntityNotFoundError(f"Бронирование {booking_id} не найдено")
        
        # Здесь вылетит BookingInvalidStatusError если статус не CHECKED_IN
        order = self.storage.create_service_order(booking.guest.id, service_type, description, price)
        booking.add_service(order)
        return order
    
    # Операция выселения и оплаты
    def check_out_guest(self, booking_id: str, payment_amount: float) -> float:
        booking = self.storage.get_booking(booking_id)
        if not booking:
            raise EntityNotFoundError(f"Бронирование {booking_id} не найдено")
        
        booking.check_out(payment_amount) # Может вылететь PaymentError или BookingInvalidStatusError
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

