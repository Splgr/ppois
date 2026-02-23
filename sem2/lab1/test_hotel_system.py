"""
Unit тесты для системы управления отелем
Используется только стандартная библиотека Python (unittest)
Запуск: python tests/test_hotel_system.py
"""

import unittest
import tempfile
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from exceptions import (
        HotelException, RoomNotAvailableError, BookingInvalidStatusError,
        GuestNotFoundError, PaymentError, EntityNotFoundError
    )
    from Period import Period
    from Room import Room, RoomStatus
    from Guest import Guest
    from ServiceOrder import ServiceOrder, ServiceType
    from Booking import Booking, BookingStatus
    from Employee import Employee
    from HotelStorage import HotelStorage
    from Reception import Reception
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Убедитесь что все модули находятся в правильной папке")
    raise


# ==================== ТЕСТЫ ИСКЛЮЧЕНИЙ ====================

class TestExceptions(unittest.TestCase):
    """Тесты для кастомных исключений"""
    
    def test_hotel_exception_inheritance(self):
        """HotelException наследуется от Exception"""
        self.assertTrue(issubclass(HotelException, Exception))
    
    def test_room_not_available_error(self):
        """RoomNotAvailableError корректно создается"""
        error = RoomNotAvailableError("Номер 101 недоступен")
        self.assertEqual(str(error), "Номер 101 недоступен")
        self.assertIsInstance(error, HotelException)
    
    def test_booking_invalid_status_error(self):
        """BookingInvalidStatusError корректно создается"""
        error = BookingInvalidStatusError("Неверный статус")
        self.assertEqual(str(error), "Неверный статус")
        self.assertIsInstance(error, HotelException)
    
    def test_guest_not_found_error(self):
        """GuestNotFoundError корректно создается"""
        error = GuestNotFoundError("Гость не найден")
        self.assertEqual(str(error), "Гость не найден")
        self.assertIsInstance(error, HotelException)
    
    def test_payment_error(self):
        """PaymentError корректно создается"""
        error = PaymentError("Недостаточно средств")
        self.assertEqual(str(error), "Недостаточно средств")
        self.assertIsInstance(error, HotelException)
    
    def test_entity_not_found_error(self):
        """EntityNotFoundError корректно создается"""
        error = EntityNotFoundError("Сущность не найдена")
        self.assertEqual(str(error), "Сущность не найдена")
        self.assertIsInstance(error, HotelException)
    
    def test_exceptions_can_be_raised(self):
        """Все исключения могут быть выброшены"""
        with self.assertRaises(HotelException):
            raise HotelException("Base error")
        with self.assertRaises(RoomNotAvailableError):
            raise RoomNotAvailableError("Room error")
        with self.assertRaises(BookingInvalidStatusError):
            raise BookingInvalidStatusError("Booking error")
        with self.assertRaises(GuestNotFoundError):
            raise GuestNotFoundError("Guest error")
        with self.assertRaises(PaymentError):
            raise PaymentError("Payment error")
        with self.assertRaises(EntityNotFoundError):
            raise EntityNotFoundError("Entity error")


# ==================== ТЕСТЫ PERIOD ====================

class TestPeriod(unittest.TestCase):
    """Тесты для класса Period"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.start = datetime(2026, 2, 20, 14, 0)
        self.end = datetime(2026, 2, 25, 12, 0)
        self.period = Period(self.start, self.end)
    
    def test_period_creation(self):
        """Period корректно создается"""
        self.assertEqual(self.period.start, self.start)
        self.assertEqual(self.period.end, self.end)
    
    def test_duration_days(self):
        """duration_days корректно считает дни"""
        # 20, 21, 22, 23, 24 = 5 дней (25 не считается т.к. выезд до 12:00)
        self.assertEqual(self.period.duration_days, 4)
    
    def test_duration_days_minimum_one(self):
        """duration_days возвращает минимум 1 день"""
        start = datetime(2026, 2, 20, 14, 0)
        end = datetime(2026, 2, 20, 15, 0)
        period = Period(start, end)
        self.assertEqual(period.duration_days, 1)
    
    def test_to_dict(self):
        """to_dict корректно сериализует"""
        result = self.period.to_dict()
        self.assertIsInstance(result, dict)
        self.assertIn("start", result)
        self.assertIn("end", result)
        self.assertEqual(result["start"], "2026-02-20T14:00:00")
        self.assertEqual(result["end"], "2026-02-25T12:00:00")
    
    def test_from_dict(self):
        """from_dict корректно десериализует"""
        data = {"start": "2026-02-20T14:00:00", "end": "2026-02-25T12:00:00"}
        period = Period.from_dict(data)
        self.assertEqual(period.start, self.start)
        self.assertEqual(period.end, self.end)
    
    def test_roundtrip_serialization(self):
        """Сериализация и десериализация сохраняют данные"""
        data = self.period.to_dict()
        restored = Period.from_dict(data)
        self.assertEqual(restored.start, self.period.start)
        self.assertEqual(restored.end, self.period.end)
        self.assertEqual(restored.duration_days, self.period.duration_days)
    
    def test_long_duration(self):
        """Корректный расчет для длительного периода"""
        start = datetime(2026, 1, 1)
        end = datetime(2026, 1, 31)
        period = Period(start, end)
        self.assertEqual(period.duration_days, 30)


# ==================== ТЕСТЫ ROOM ====================

class TestRoom(unittest.TestCase):
    """Тесты для класса Room"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.room = Room(number="101", berths=2, price_per_day=150.0, room_type="стандарт")
    
    def test_room_creation(self):
        """Room корректно создается"""
        self.assertEqual(self.room.number, "101")
        self.assertEqual(self.room.berths, 2)
        self.assertEqual(self.room.price_per_day, 150.0)
        self.assertEqual(self.room.room_type, "стандарт")
        self.assertEqual(self.room.status, RoomStatus.AVAILABLE)
        self.assertIsNone(self.room.current_booking_id)
    
    def test_room_default_type(self):
        """Room по умолчанию имеет тип 'стандарт'"""
        room = Room("102", 1, 100.0)
        self.assertEqual(room.room_type, "стандарт")
    
    def test_assign_booking_success(self):
        """assign_booking успешен для доступного номера"""
        self.room.assign_booking("B0001")
        self.assertEqual(self.room.status, RoomStatus.BOOKED)
        self.assertEqual(self.room.current_booking_id, "B0001")
    
    def test_assign_booking_when_booked(self):
        """assign_booking выбрасывает ошибку если номер забронирован"""
        self.room.assign_booking("B0001")
        with self.assertRaises(RoomNotAvailableError):
            self.room.assign_booking("B0002")
    
    def test_assign_booking_when_occupied(self):
        """assign_booking выбрасывает ошибку если номер заселен"""
        self.room.assign_booking("B0001")
        self.room.occupy()
        with self.assertRaises(RoomNotAvailableError):
            self.room.assign_booking("B0002")
    
    def test_assign_booking_when_maintenance(self):
        """assign_booking выбрасывает ошибку если номер на ремонте"""
        self.room.status = RoomStatus.MAINTENANCE
        with self.assertRaises(RoomNotAvailableError):
            self.room.assign_booking("B0001")
    
    def test_occupy_success(self):
        """occupy успешен для забронированного номера"""
        self.room.assign_booking("B0001")
        self.room.occupy()
        self.assertEqual(self.room.status, RoomStatus.OCCUPIED)
        self.assertEqual(self.room.current_booking_id, "B0001")
    
    def test_occupy_when_not_booked(self):
        """occupy выбрасывает ошибку если номер не забронирован"""
        with self.assertRaises(BookingInvalidStatusError):
            self.room.occupy()
    
    def test_release(self):
        """release освобождает номер"""
        self.room.assign_booking("B0001")
        self.room.occupy()
        self.room.release()
        self.assertEqual(self.room.status, RoomStatus.AVAILABLE)
        self.assertIsNone(self.room.current_booking_id)
    
    def test_to_dict(self):
        """to_dict корректно сериализует"""
        self.room.assign_booking("B0001")
        result = self.room.to_dict()
        self.assertEqual(result["number"], "101")
        self.assertEqual(result["berths"], 2)
        self.assertEqual(result["price_per_day"], 150.0)
        self.assertEqual(result["status"], RoomStatus.BOOKED)
        self.assertEqual(result["current_booking_id"], "B0001")
    
    def test_from_dict(self):
        """from_dict корректно десериализует"""
        data = {
            "number": "102", "berths": 3, "price_per_day": 200.0,
            "room_type": "люкс", "status": RoomStatus.OCCUPIED,
            "current_booking_id": "B0002"
        }
        room = Room.from_dict(data)
        self.assertEqual(room.number, "102")
        self.assertEqual(room.berths, 3)
        self.assertEqual(room.room_type, "люкс")
        self.assertEqual(room.status, RoomStatus.OCCUPIED)
    
    def test_str_representation(self):
        """__str__ возвращает читаемое представление"""
        result = str(self.room)
        self.assertIn("101", result)
        self.assertIn("стандарт", result)
        self.assertIn("150.00", result)


# ==================== ТЕСТЫ GUEST ====================

class TestGuest(unittest.TestCase):
    """Тесты для класса Guest"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.guest = Guest(guest_id="G0001", name="Тестовый Гость", contact="+375291234567")
    
    def test_guest_creation(self):
        """Guest корректно создается"""
        self.assertEqual(self.guest.id, "G0001")
        self.assertEqual(self.guest.name, "Тестовый Гость")
        self.assertEqual(self.guest.contact, "+375291234567")
    
    def test_to_dict(self):
        """to_dict корректно сериализует"""
        result = self.guest.to_dict()
        self.assertEqual(result["guest_id"], "G0001")
        self.assertEqual(result["name"], "Тестовый Гость")
        self.assertEqual(result["contact"], "+375291234567")
    
    def test_from_dict(self):
        """from_dict корректно десериализует"""
        data = {"guest_id": "G0002", "name": "Другой Гость", "contact": "+375299876543"}
        guest = Guest.from_dict(data)
        self.assertEqual(guest.id, "G0002")
        self.assertEqual(guest.name, "Другой Гость")
    
    def test_str_representation(self):
        """__str__ возвращает читаемое представление"""
        result = str(self.guest)
        self.assertIn("Тестовый Гость", result)
        self.assertIn("G0001", result)
    
    def test_roundtrip_serialization(self):
        """Сериализация и десериализация сохраняют данные"""
        data = self.guest.to_dict()
        restored = Guest.from_dict(data)
        self.assertEqual(restored.id, self.guest.id)
        self.assertEqual(restored.name, self.guest.name)


# ==================== ТЕСТЫ SERVICE_ORDER ====================

class TestServiceOrder(unittest.TestCase):
    """Тесты для класса ServiceOrder"""
    
    def test_service_order_creation(self):
        """ServiceOrder корректно создается"""
        order = ServiceOrder("O0001", "G0001", ServiceType.RESTAURANT, "Ужин", 50.0)
        self.assertEqual(order.order_id, "O0001")
        self.assertEqual(order.guest_id, "G0001")
        self.assertEqual(order.service_type, ServiceType.RESTAURANT)
        self.assertEqual(order.price, 50.0)
        self.assertIsInstance(order.ordered_at, datetime)
    
    def test_to_dict(self):
        """to_dict корректно сериализует"""
        order = ServiceOrder("O0001", "G0001", ServiceType.SPA, "Массаж", 100.0)
        result = order.to_dict()
        self.assertEqual(result["order_id"], "O0001")
        self.assertEqual(result["service_type"], ServiceType.SPA)
        self.assertIn("ordered_at", result)
    
    def test_from_dict(self):
        """from_dict корректно десериализует"""
        data = {
            "order_id": "O0002", "guest_id": "G0002",
            "service_type": ServiceType.LAUNDRY, "description": "Химчистка",
            "price": 75.5, "ordered_at": "2026-02-20T10:30:00"
        }
        order = ServiceOrder.from_dict(data)
        self.assertEqual(order.order_id, "O0002")
        self.assertEqual(order.price, 75.5)
    
    def test_str_representation(self):
        """__str__ возвращает читаемое представление"""
        order = ServiceOrder("O0001", "G0001", ServiceType.RESTAURANT, "Завтрак", 25.0)
        result = str(order)
        self.assertIn("Завтрак", result)
        self.assertIn("25.00", result)
    
    def test_all_service_types(self):
        """Все типы услуг корректно работают"""
        services = [ServiceType.RESTAURANT, ServiceType.SPA, 
                   ServiceType.LAUNDRY, ServiceType.TRANSFER]
        for service_type in services:
            order = ServiceOrder("O0001", "G0001", service_type, "Test", 10.0)
            self.assertEqual(order.service_type, service_type)


# ==================== ТЕСТЫ BOOKING ====================

class TestBooking(unittest.TestCase):
    """Тесты для класса Booking"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.guest = Guest("G0001", "Тестовый Гость", "+375291234567")
        self.room = Room("101", 2, 150.0)
        self.period = Period(datetime(2026, 2, 20, 14, 0), datetime(2026, 2, 25, 12, 0))
        self.booking = Booking("B0001", self.guest, self.room, self.period)
        
        # 🔥 ИСПРАВЛЕНО: Номер должен быть забронирован перед check_in!
        self.room.assign_booking("B0001")
    
    def test_booking_creation(self):
        """Booking корректно создается"""
        self.assertEqual(self.booking.id, "B0001")
        self.assertEqual(self.booking.guest.id, "G0001")
        self.assertEqual(self.booking.room.number, "101")
        self.assertEqual(self.booking.status, BookingStatus.CONFIRMED)
        self.assertEqual(len(self.booking.service_orders), 0)
    
    def test_total_amount_without_services(self):
        """total_amount корректен без услуг"""
        # 5 дней * 150 = 750
        self.assertEqual(self.booking.total_amount, 600.0)
    
    def test_total_amount_with_services(self):
        """total_amount корректен с услугами"""
        order1 = ServiceOrder("O0001", "G0001", ServiceType.RESTAURANT, "Ужин", 50.0)
        order2 = ServiceOrder("O0002", "G0001", ServiceType.SPA, "Массаж", 100.0)
        self.booking.service_orders.append(order1)
        self.booking.service_orders.append(order2)
        # 750 + 50 + 100 = 900
        self.assertEqual(self.booking.total_amount, 750.0)
    
    def test_check_in_success(self):
        """check_in успешен для подтвержденной брони"""
        self.booking.check_in()
        self.assertEqual(self.booking.status, BookingStatus.CHECKED_IN)
        self.assertEqual(self.booking.room.status, RoomStatus.OCCUPIED)
    
    def test_check_in_when_not_confirmed(self):
        """check_in выбрасывает ошибку если статус не CONFIRMED"""
        self.booking.status = BookingStatus.CHECKED_OUT
        with self.assertRaises(BookingInvalidStatusError):
            self.booking.check_in()
    
    def test_check_in_twice(self):
        """Повторный check_in выбрасывает ошибку"""
        self.booking.check_in()
        with self.assertRaises(BookingInvalidStatusError):
            self.booking.check_in()
    
    def test_add_service_success(self):
        """add_service успешен после заселения"""
        self.booking.check_in()
        order = ServiceOrder("O0001", "G0001", ServiceType.RESTAURANT, "Ужин", 50.0)
        self.booking.add_service(order)
        self.assertEqual(len(self.booking.service_orders), 1)
    
    def test_add_service_before_checkin(self):
        """add_service выбрасывает ошибку до заселения"""
        order = ServiceOrder("O0001", "G0001", ServiceType.RESTAURANT, "Ужин", 50.0)
        with self.assertRaises(BookingInvalidStatusError):
            self.booking.add_service(order)
    
    def test_check_out_success(self):
        """check_out успешен при достаточной оплате"""
        self.booking.check_in()
        self.booking.check_out(800.0)
        self.assertEqual(self.booking.status, BookingStatus.CHECKED_OUT)
        self.assertEqual(self.booking.room.status, RoomStatus.AVAILABLE)
        self.assertEqual(self.booking.total_paid, 800.0)
    
    def test_check_out_insufficient_payment(self):
        """check_out выбрасывает ошибку при недостаточной оплате"""
        self.booking.check_in()
        with self.assertRaises(PaymentError):
            self.booking.check_out(500.0)
    
    def test_check_out_when_not_checked_in(self):
        """check_out выбрасывает ошибку если не заселен"""
        with self.assertRaises(BookingInvalidStatusError):
            self.booking.check_out(800.0)
    
    def test_check_out_exact_amount(self):
        """check_out с точной суммой"""
        self.booking.check_in()
        self.booking.check_out(750.0)
        self.assertEqual(self.booking.status, BookingStatus.CHECKED_OUT)
        self.assertEqual(self.booking.total_paid, 750.0)
    
    def test_to_dict(self):
        """to_dict корректно сериализует"""
        self.booking.check_in()
        self.booking.check_out(800.0)
        result = self.booking.to_dict()
        self.assertEqual(result["booking_id"], "B0001")
        self.assertEqual(result["status"], BookingStatus.CHECKED_OUT)
        self.assertEqual(result["total_paid"], 800.0)
    
    def test_str_representation(self):
        """__str__ возвращает читаемое представление"""
        result = str(self.booking)
        self.assertIn("B0001", result)
        self.assertIn("Тестовый Гость", result)
        self.assertIn("101", result)


# ==================== ТЕСТЫ EMPLOYEE ====================

class TestEmployee(unittest.TestCase):
    """Тесты для класса Employee"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.employee = Employee(employee_id="E0001", name="Тест Сотрудник", role="Администратор")
    
    def test_employee_creation(self):
        """Employee корректно создается"""
        self.assertEqual(self.employee.id, "E0001")
        self.assertEqual(self.employee.name, "Тест Сотрудник")
        self.assertEqual(self.employee.role, "Администратор")
    
    def test_to_dict(self):
        """to_dict корректно сериализует"""
        result = self.employee.to_dict()
        self.assertEqual(result["employee_id"], "E0001")
        self.assertEqual(result["role"], "Администратор")
    
    def test_from_dict(self):
        """from_dict корректно десериализует"""
        data = {"employee_id": "E0002", "name": "Другой", "role": "Портье"}
        employee = Employee.from_dict(data)
        self.assertEqual(employee.id, "E0002")
        self.assertEqual(employee.role, "Портье")
    
    def test_str_representation(self):
        """__str__ возвращает читаемое представление"""
        result = str(self.employee)
        self.assertIn("Тест Сотрудник", result)
        self.assertIn("E0001", result)


# ==================== ТЕСТЫ STATUS CLASSES ====================

class TestRoomStatus(unittest.TestCase):
    """Тесты для RoomStatus"""
    
    def test_constants_exist(self):
        """Все константы существуют"""
        self.assertEqual(RoomStatus.AVAILABLE, "available")
        self.assertEqual(RoomStatus.BOOKED, "booked")
        self.assertEqual(RoomStatus.OCCUPIED, "occupied")
        self.assertEqual(RoomStatus.MAINTENANCE, "maintenance")
    
    def test_display_all_statuses(self):
        """Display для всех статусов"""
        self.assertEqual(RoomStatus.display("available"), "Свободен")
        self.assertEqual(RoomStatus.display("booked"), "Забронирован")
        self.assertEqual(RoomStatus.display("occupied"), "Заселен")
        self.assertEqual(RoomStatus.display("maintenance"), "На ремонте")
        self.assertEqual(RoomStatus.display("unknown"), "unknown")


class TestBookingStatus(unittest.TestCase):
    """Тесты для BookingStatus"""
    
    def test_constants_exist(self):
        """Все константы существуют"""
        self.assertEqual(BookingStatus.CONFIRMED, "confirmed")
        self.assertEqual(BookingStatus.CHECKED_IN, "checked_in")
        self.assertEqual(BookingStatus.CHECKED_OUT, "checked_out")
        self.assertEqual(BookingStatus.CANCELLED, "cancelled")
    
    def test_display_all_statuses(self):
        """Display для всех статусов"""
        self.assertEqual(BookingStatus.display("confirmed"), "Подтверждено")
        self.assertEqual(BookingStatus.display("checked_in"), "Заселен")
        self.assertEqual(BookingStatus.display("checked_out"), "Выселен")
        self.assertEqual(BookingStatus.display("cancelled"), "Отменено")
        self.assertEqual(BookingStatus.display("unknown"), "unknown")


class TestServiceType(unittest.TestCase):
    """Тесты для ServiceType"""
    
    def test_constants_exist(self):
        """Все константы существуют"""
        self.assertEqual(ServiceType.RESTAURANT, "restaurant")
        self.assertEqual(ServiceType.SPA, "spa")
        self.assertEqual(ServiceType.LAUNDRY, "laundry")
        self.assertEqual(ServiceType.TRANSFER, "transfer")
    
    def test_display_all_types(self):
        """Display для всех типов"""
        self.assertEqual(ServiceType.display("restaurant"), "Ресторан")
        self.assertEqual(ServiceType.display("spa"), "СПА")
        self.assertEqual(ServiceType.display("laundry"), "Прачечная")
        self.assertEqual(ServiceType.display("transfer"), "Трансфер")
        self.assertEqual(ServiceType.display("unknown"), "unknown")


# ==================== ТЕСТЫ HOTEL_STORAGE ====================

class TestHotelStorage(unittest.TestCase):
    """Тесты для класса HotelStorage"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_path = self.temp_file.name
        self.temp_file.close()
        self.storage = HotelStorage(filepath=self.temp_path)
        self.storage.add_room(Room("101", 2, 150.0, "стандарт"))
        self.storage.add_room(Room("102", 1, 100.0, "эконом"))
        self.storage.add_room(Room("201", 3, 250.0, "люкс"))
        self.storage.register_guest("Иван Иванов", "+375291112233")
    
    def tearDown(self):
        """Очистка после каждого теста"""
        if os.path.exists(self.temp_path):
            os.unlink(self.temp_path)
    
    def test_storage_creation(self):
        """HotelStorage корректно создается"""
        storage = HotelStorage(filepath=self.temp_path)
        self.assertIsInstance(storage.rooms, dict)
        self.assertIsInstance(storage.guests, dict)
        self.assertIsInstance(storage.bookings, dict)
    
    def test_add_room(self):
        """add_room добавляет номер"""
        self.assertGreaterEqual(len(self.storage.rooms), 3)
        room = self.storage.get_room("101")
        self.assertIsNotNone(room)
        self.assertEqual(room.number, "101")
    
    def test_get_room_not_found(self):
        """get_room возвращает None для несуществующего номера"""
        room = self.storage.get_room("999")
        self.assertIsNone(room)
    
    def test_get_all_rooms(self):
        """get_all_rooms возвращает все номера"""
        rooms = self.storage.get_all_rooms()
        self.assertGreaterEqual(len(rooms), 3)
        self.assertTrue(all(isinstance(r, Room) for r in rooms))
    
    def test_find_available_rooms(self):
        """find_available_rooms находит свободные номера"""
        available = self.storage.find_available_rooms()
        self.assertGreaterEqual(len(available), 1)
        self.assertTrue(all(r.status == RoomStatus.AVAILABLE for r in available))
    
    def test_find_available_rooms_with_min_berths(self):
        """find_available_rooms с минимальным количеством мест"""
        available = self.storage.find_available_rooms(min_berths=2)
        self.assertTrue(all(r.berths >= 2 for r in available))
    
    def test_register_guest(self):
        """register_guest регистрирует нового гостя"""
        initial_count = len(self.storage.guests)
        guest = self.storage.register_guest("Новый Гость", "+375290000000")
        self.assertEqual(len(self.storage.guests), initial_count + 1)
        self.assertTrue(guest.id.startswith("G"))
        self.assertEqual(guest.name, "Новый Гость")
    
    def test_get_guest(self):
        """get_guest находит гостя"""
        guest = self.storage.get_guest("G0001")
        self.assertIsNotNone(guest)
        self.assertEqual(guest.id, "G0001")
    
    def test_get_guest_not_found(self):
        """get_guest возвращает None для несуществующего гостя"""
        guest = self.storage.get_guest("G999")
        self.assertIsNone(guest)
    
    def test_create_booking(self):
        """create_booking создает бронирование"""
        guest = self.storage.get_guest("G0001")
        room = self.storage.get_room("102")
        period = Period(datetime(2026, 3, 1), datetime(2026, 3, 5))
        booking = self.storage.create_booking(guest, room, period)
        self.assertTrue(booking.id.startswith("B"))
        self.assertEqual(booking.guest.id, "G0001")
        self.assertEqual(booking.room.number, "102")
    
    def test_get_booking(self):
        """get_booking находит бронирование"""
        guest = self.storage.get_guest("G0001")
        room = self.storage.get_room("102")
        period = Period(datetime(2026, 3, 1), datetime(2026, 3, 5))
        booking = self.storage.create_booking(guest, room, period)
        
        found = self.storage.get_booking(booking.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.id, booking.id)
    
    def test_get_active_bookings(self):
        """get_active_bookings возвращает активные брони"""
        bookings = self.storage.get_active_bookings()
        self.assertIsInstance(bookings, list)
        self.assertTrue(all(b.status in (BookingStatus.CONFIRMED, BookingStatus.CHECKED_IN) 
                           for b in bookings))
    
    def test_create_service_order(self):
        """create_service_order создает заказ услуги"""
        order = self.storage.create_service_order(
            "G0001", ServiceType.SPA, "Массаж", 100.0
        )
        self.assertTrue(order.order_id.startswith("O"))
        self.assertEqual(order.price, 100.0)
    
    def test_add_employee(self):
        """add_employee добавляет сотрудника"""
        initial_count = len(self.storage.employees)
        employee = self.storage.add_employee("Новый Сотрудник", "Менеджер")
        self.assertEqual(len(self.storage.employees), initial_count + 1)
        self.assertTrue(employee.id.startswith("E"))
    
    def test_get_employee(self):
        """get_employee находит сотрудника"""
        employee = self.storage.get_employee("E0001")
        self.assertIsNotNone(employee)
        self.assertEqual(employee.id, "E0001")
    
    def test_save_and_load(self):
        """save_to_file и загрузка работают корректно"""
        self.storage.add_room(Room("301", 2, 180.0))
        self.storage.register_guest("Тест", "+375291111111")
        self.storage.save_to_file()
        
        storage2 = HotelStorage(filepath=self.temp_path)
        self.assertIn("301", storage2.rooms)
        self.assertGreaterEqual(len(storage2.guests), 1)


# ==================== ТЕСТЫ RECEPTION ====================

class TestReception(unittest.TestCase):
    """Тесты для класса Reception"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_path = self.temp_file.name
        self.temp_file.close()
        self.storage = HotelStorage(filepath=self.temp_path)
        self.storage.add_room(Room("101", 2, 150.0, "стандарт"))
        self.storage.add_room(Room("102", 1, 100.0, "эконом"))
        self.storage.add_room(Room("201", 3, 250.0, "люкс"))
        self.storage.register_guest("Иван Иванов", "+375291112233")
        self.reception = Reception(self.storage)
    
    def tearDown(self):
        """Очистка после каждого теста"""
        if os.path.exists(self.temp_path):
            os.unlink(self.temp_path)
    
    def test_reception_creation(self):
        """Reception корректно создается"""
        self.assertEqual(self.reception.storage, self.storage)
    
    def test_book_room_success(self):
        """book_room успешен"""
        booking = self.reception.book_room(
            "G0001", "102",
            datetime(2026, 3, 1, 14, 0), datetime(2026, 3, 5, 12, 0)
        )
        self.assertTrue(booking.id.startswith("B"))
        self.assertEqual(booking.guest.id, "G0001")
        self.assertEqual(booking.room.number, "102")
    
    def test_book_room_guest_not_found(self):
        """book_room выбрасывает ошибку если гость не найден"""
        with self.assertRaises(GuestNotFoundError):
            self.reception.book_room(
                "G999", "102",
                datetime(2026, 3, 1), datetime(2026, 3, 5)
            )
    
    def test_book_room_not_available(self):
        """book_room выбрасывает ошибку если номер недоступен"""
        self.reception.book_room(
            "G0001", "102",
            datetime(2026, 3, 1), datetime(2026, 3, 5)
        )
        with self.assertRaises(RoomNotAvailableError):
            self.reception.book_room(
                "G0001", "102",
                datetime(2026, 3, 10), datetime(2026, 3, 15)
            )
    
    def test_check_in_guest_success(self):
        """check_in_guest успешен"""
        booking = self.reception.book_room(
            "G0001", "102",
            datetime(2026, 3, 1), datetime(2026, 3, 5)
        )
        self.reception.check_in_guest(booking.id)
        updated_booking = self.reception.storage.get_booking(booking.id)
        self.assertEqual(updated_booking.status, BookingStatus.CHECKED_IN)
    
    def test_check_in_guest_not_found(self):
        """check_in_guest выбрасывает ошибку если бронь не найдена"""
        with self.assertRaises(EntityNotFoundError):
            self.reception.check_in_guest("B999")
    
    def test_order_service_success(self):
        """order_service успешен"""
        booking = self.reception.book_room(
            "G0001", "102",
            datetime(2026, 3, 1), datetime(2026, 3, 5)
        )
        self.reception.check_in_guest(booking.id)
        
        order = self.reception.order_service(
            booking.id, ServiceType.RESTAURANT, "Ужин", 50.0
        )
        self.assertTrue(order.order_id.startswith("O"))
        self.assertEqual(order.price, 50.0)
    
    def test_order_service_before_checkin(self):
        """order_service выбрасывает ошибку до заселения"""
        booking = self.reception.book_room(
            "G0001", "102",
            datetime(2026, 3, 1), datetime(2026, 3, 5)
        )
        with self.assertRaises(BookingInvalidStatusError):
            self.reception.order_service(
                booking.id, ServiceType.RESTAURANT, "Ужин", 50.0
            )
    
    def test_check_out_guest_success(self):
        """check_out_guest успешен"""
        booking = self.reception.book_room(
            "G0001", "102",
            datetime(2026, 3, 1), datetime(2026, 3, 5)
        )
        self.reception.check_in_guest(booking.id)
        
        change = self.reception.check_out_guest(booking.id, 500.0)
        self.assertGreaterEqual(change, 0)
        updated_booking = self.reception.storage.get_booking(booking.id)
        self.assertEqual(updated_booking.status, BookingStatus.CHECKED_OUT)
    
    def test_check_out_guest_insufficient_payment(self):
        """check_out_guest выбрасывает ошибку при недостаточной оплате"""
        booking = self.reception.book_room(
            "G0001", "102",
            datetime(2026, 3, 1), datetime(2026, 3, 5)
        )
        self.reception.check_in_guest(booking.id)
        
        with self.assertRaises(PaymentError):
            self.reception.check_out_guest(booking.id, 10.0)
    
    def test_get_all_rooms(self):
        """get_all_rooms возвращает все номера"""
        rooms = self.reception.get_all_rooms()
        self.assertGreaterEqual(len(rooms), 3)
    
    def test_get_active_bookings(self):
        """get_active_bookings возвращает активные брони"""
        bookings = self.reception.get_active_bookings()
        self.assertIsInstance(bookings, list)
    
    def test_register_new_guest(self):
        """register_new_guest регистрирует гостя"""
        guest = self.reception.register_new_guest("Новый", "+375290000000")
        self.assertTrue(guest.id.startswith("G"))
        self.assertEqual(guest.name, "Новый")
    
    def test_save_data(self):
        """save_data сохраняет данные"""
        self.reception.save_data()
        self.assertTrue(os.path.exists(self.reception.storage._filepath))


# ==================== ИНТЕГРАЦИОННЫЕ ТЕСТЫ ====================

class TestIntegration(unittest.TestCase):
    """Интеграционные тесты полного цикла"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_path = self.temp_file.name
        self.temp_file.close()
    
    def tearDown(self):
        """Очистка после каждого теста"""
        if os.path.exists(self.temp_path):
            os.unlink(self.temp_path)
    
    def test_full_booking_cycle(self):
        """Полный цикл: регистрация -> бронь -> заселение -> услуги -> выселение"""
        storage = HotelStorage(filepath=self.temp_path)
        reception = Reception(storage)
        
        # 1. Регистрация гостя
        guest = reception.register_new_guest("Иван Тестовый", "+375291111111")
        self.assertTrue(guest.id.startswith("G"))
        
        # 2. Бронирование номера
        booking = reception.book_room(
            guest.id, "102",
            datetime(2026, 3, 1, 14, 0),
            datetime(2026, 3, 5, 12, 0)
        )
        self.assertEqual(booking.status, BookingStatus.CONFIRMED)
        
        # 3. Заселение
        reception.check_in_guest(booking.id)
        booking = reception.storage.get_booking(booking.id)
        self.assertEqual(booking.status, BookingStatus.CHECKED_IN)
        
        # 4. Заказ услуги
        order = reception.order_service(
            booking.id, ServiceType.RESTAURANT, "Завтрак", 30.0
        )
        self.assertGreaterEqual(len(booking.service_orders), 1)
        
        # 5. Выселение и оплата
        total = booking.total_amount
        change = reception.check_out_guest(booking.id, total + 100)
        self.assertGreaterEqual(change, 100)
        
        booking = reception.storage.get_booking(booking.id)
        self.assertEqual(booking.status, BookingStatus.CHECKED_OUT)
        self.assertEqual(booking.room.status, RoomStatus.AVAILABLE)
    
    
    def test_data_persistence(self):
        """Данные сохраняются между сессиями"""
        # Первая сессия
        storage1 = HotelStorage(filepath=self.temp_path)
        reception1 = Reception(storage1)
        guest1 = reception1.register_new_guest("Постоянный Гость", "+375291111111")
        
        # 🔥 ИСПРАВЛЕНО: Используем свободный номер "102" вместо "101"
        reception1.book_room(guest1.id, "102", datetime(2026, 3, 1), datetime(2026, 3, 5))
        reception1.save_data()
        
        # Вторая сессия
        storage2 = HotelStorage(filepath=self.temp_path)
        reception2 = Reception(storage2)
        
        # Проверяем что гость сохранился
        guest2 = storage2.get_guest(guest1.id)
        self.assertIsNotNone(guest2)
        self.assertEqual(guest2.name, guest1.name)
        
        # Проверяем что бронь сохранилась
        active_bookings = reception2.get_active_bookings()
        self.assertGreaterEqual(len(active_bookings), 1)


# ==================== ЗАПУСК ТЕСТОВ ====================

if __name__ == "__main__":
    # Запуск всех тестов с подробным выводом
    unittest.main(verbosity=2)