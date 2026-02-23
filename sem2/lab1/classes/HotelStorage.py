from Room import Room 
from Guest import Guest
from Booking import Booking
from Employee import Employee
from RoomStatus import RoomStatus
from BookingStatus import BookingStatus
from datetime import datetime
import json
from Period import Period
from ServiceOrder import ServiceOrder
from ServiceType import ServiceType
from pathlib import Path

class HotelStorage:
    """Хранилище всех данных отеля"""
    
    def __init__(self, filepath: str = "hotel_data.json"):
        self._filepath = Path(filepath)
        self.rooms: dict[str, Room] = {}
        self.guests: dict[str, Guest] = {}
        self.bookings: dict[str, Booking] = {}
        self.employees: dict[str, Employee] = {}
        self._next_guest_id = 1
        self._next_booking_id = 1
        self._next_order_id = 1
        self._next_employee_id = 1
        
        self._load_or_initialize()
    
    def _load_or_initialize(self):
        if self._filepath.exists():
            try:
                self._load_from_file()
                print(f"Данные загружены из {self._filepath}")
                return
            except Exception as e:
                print(f"Ошибка загрузки: {e}. Создаём новую базу...")
                self._filepath.unlink(missing_ok=True)
        
        self._initialize_demo_data()
        self.save_to_file()
        print(f"Создан новый файл {self._filepath} с демо-данными")
    
    def _load_from_file(self):
        data = json.loads(self._filepath.read_text(encoding="utf-8"))
        
        for room_data in data.get("rooms", []):
            room = Room.from_dict(room_data)
            self.rooms[room.number] = room
        
        self._next_guest_id = data.get("next_guest_id", 1)
        for guest_data in data.get("guests", []):
            guest = Guest.from_dict(guest_data)
            self.guests[guest.id] = guest
        
        self._next_booking_id = data.get("next_booking_id", 1)
        self._next_order_id = data.get("next_order_id", 1)
        for booking_data in data.get("bookings", []):
            guest = self.guests.get(booking_data["guest_id"])
            room = self.rooms.get(booking_data["room_number"])
            if guest and room:
                booking = Booking.from_dict(booking_data, guest, room)
                self.bookings[booking.id] = booking
                if booking.status == BookingStatus.CHECKED_IN:
                    room.status = RoomStatus.OCCUPIED
                    room.current_booking_id = booking.id
                elif booking.status == BookingStatus.CONFIRMED:
                    room.status = RoomStatus.BOOKED
                    room.current_booking_id = booking.id
        
        self._next_employee_id = data.get("next_employee_id", 1)
        for employee_data in data.get("employees", []):
            employee = Employee.from_dict(employee_data)
            self.employees[employee.id] = employee
        
        print(f"Загружено: {len(self.rooms)} номеров, {len(self.guests)} гостей, {len(self.bookings)} бронирований")
    
    def _initialize_demo_data(self):
        # Номера
        rooms_data = [
            ("101", 2, 150.0, "стандарт"),
            ("102", 1, 100.0, "эконом"),
            ("103", 2, 160.0, "стандарт"),
            ("201", 3, 250.0, "люкс"),
            ("202", 2, 200.0, "улучшенный"),
        ]
        for number, berths, price, r_type in rooms_data:
            self.rooms[number] = Room(number, berths, price, r_type)
        
        # Гости
        self.guests["G0001"] = Guest("G0001", "Анна Сидорова", "+375291112233")
        self.guests["G0002"] = Guest("G0002", "Максим Иванов", "+375294445566")
        self._next_guest_id = 3
        
        # Бронирования
        period = Period(
            datetime(2026, 2, 15, 14, 0),
            datetime(2026, 2, 18, 12, 0)
        )
        booking = Booking("B0001", self.guests["G0001"], self.rooms["101"], period)
        self.bookings["B0001"] = booking
        self.rooms["101"].assign_booking("B0001")
        booking.check_in()
        
        # Услуга
        order = ServiceOrder("O0001", "G0001", ServiceType.RESTAURANT, "Ужин в ресторане", 45.50)
        booking.add_service(order)
        self._next_order_id = 2
        self._next_booking_id = 2
        
        # Персонал
        self.employees["E0001"] = Employee("E0001", "Иван Петров", "Администратор")
        self.employees["E0002"] = Employee("E0002", "Мария Соколова", "Портье")
        self._next_employee_id = 3
    
    def save_to_file(self):
        try:
            data = {
                "rooms": [room.to_dict() for room in self.rooms.values()],
                "guests": [guest.to_dict() for guest in self.guests.values()],
                "bookings": [booking.to_dict() for booking in self.bookings.values()],
                "employees": [employee.to_dict() for employee in self.employees.values()],
                "next_guest_id": self._next_guest_id,
                "next_booking_id": self._next_booking_id,
                "next_order_id": self._next_order_id,
                "next_employee_id": self._next_employee_id
            }
            self._filepath.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"Данные сохранены в {self._filepath}")
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
    
    # Методы для работы с номерами
    def add_room(self, room: Room):
        self.rooms[room.number] = room
    
    def get_room(self, number: str) -> Room | None:
        return self.rooms.get(number)
    
    def get_all_rooms(self) -> list[Room]:
        return list(self.rooms.values())
    
    def find_available_rooms(self, min_berths: int = 1) -> list[Room]:
        return [r for r in self.rooms.values() if r.status == RoomStatus.AVAILABLE and r.berths >= min_berths]
    
    # Методы для работы с гостями
    def register_guest(self, name: str, contact: str) -> Guest:
        guest_id = f"G{self._next_guest_id:04d}"
        self._next_guest_id += 1
        guest = Guest(guest_id, name, contact)
        self.guests[guest_id] = guest
        return guest
    
    def get_guest(self, guest_id: str) -> Guest | None:
        return self.guests.get(guest_id)
    
    # Методы для работы с бронированиями
    def create_booking(self, guest: Guest, room: Room, period: Period) -> Booking:
        booking_id = f"B{self._next_booking_id:04d}"
        self._next_booking_id += 1
        booking = Booking(booking_id, guest, room, period)
        self.bookings[booking_id] = booking
        return booking
    
    def get_booking(self, booking_id: str) -> Booking | None:
        return self.bookings.get(booking_id)
    
    def get_active_bookings(self) -> list[Booking]:
        return [b for b in self.bookings.values() 
                if b.status in (BookingStatus.CONFIRMED, BookingStatus.CHECKED_IN)]
    
    def get_bookings_by_guest(self, guest_id: str) -> list[Booking]:
        return [b for b in self.bookings.values() if b.guest.id == guest_id]
    
    # Методы для работы с услугами
    def create_service_order(self, guest_id: str, service_type: str, description: str, price: float) -> ServiceOrder:
        order_id = f"O{self._next_order_id:04d}"
        self._next_order_id += 1
        return ServiceOrder(order_id, guest_id, service_type, description, price)
    
    # Методы для работы с персоналом
    def add_employee(self, name: str, role: str) -> Employee:
        employee_id = f"E{self._next_employee_id:04d}"
        self._next_employee_id += 1
        employee = Employee(employee_id, name, role)
        self.employees[employee_id] = employee
        return employee
    
    def get_employee(self, employee_id: str) -> Employee | None:
        return self.employees.get(employee_id)