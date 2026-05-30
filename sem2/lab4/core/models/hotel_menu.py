from reception import Reception
from .room_status import RoomStatus
import os
from datetime import datetime
from ..exceptions import HotelException
from .booking_status import BookingStatus

class HotelMenu:
    """Интерактивное меню"""
    
    def __init__(self, reception: Reception):
        self.reception = reception
        self.running = True
    
    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _pause(self):
        input("\nНажмите Enter для продолжения...")
    
    def display_rooms(self):
        self._clear_screen()
        rooms = self.reception.get_all_rooms()
        print("\n" + "="*80)
        print("СПИСОК НОМЕРОВ ОТЕЛЯ")
        print("="*80)
        
        if not rooms:
            print("В отеле пока нет номеров")
            self._pause()
            return
        
        groups = {
            RoomStatus.AVAILABLE: [],
            RoomStatus.BOOKED: [],
            RoomStatus.OCCUPIED: [],
            RoomStatus.MAINTENANCE: []
        }
        for room in rooms:
            groups[room.status].append(room)
        
        total = len(rooms)
        for status in [RoomStatus.AVAILABLE, RoomStatus.BOOKED, RoomStatus.OCCUPIED, RoomStatus.MAINTENANCE]:
            rooms_list = groups[status]
            if rooms_list:
                count = len(rooms_list)
                print(f"\n{RoomStatus.display(status)} ({count} из {total}, {count/total*100:.1f}%):")
                for room in rooms_list:
                    info = f"  * {room}"
                    if room.current_booking_id:
                        booking = self.reception.storage.get_booking(room.current_booking_id)
                        if booking:
                            guest_info = f" -> Бронь #{booking.id}, гость: {booking.guest.name}"
                            info += guest_info
                    print(info)
        
        print("\n" + "="*80)
        self._pause()
    
    def display_bookings(self):
        self._clear_screen()
        bookings = self.reception.get_active_bookings()
        print("\n" + "="*80)
        print("АКТИВНЫЕ БРОНИРОВАНИЯ")
        print("="*80)
        
        if not bookings:
            print("Нет активных бронирований")
            self._pause()
            return
        
        for i, booking in enumerate(bookings, 1):
            print(f"\n{i}. {booking}")
            if booking.service_orders:
                print("   Дополнительные услуги:")
                for order in booking.service_orders:
                    print(f"     * {order}")
        
        print("\n" + "="*80)
        self._pause()
    
    def register_guest_flow(self):
        self._clear_screen()
        print("\nРЕГИСТРАЦИЯ НОВОГО ГОСТЯ")
        print("-" * 80)
        name = input("  Имя гостя: ").strip()
        contact = input("  Контактный телефон: ").strip()
        
        if not name or not contact:
            print("\nОшибка: имя и телефон обязательны")
            self._pause()
            return
        
        try:
            guest = self.reception.register_new_guest(name, contact)
            print(f"\nГость успешно зарегистрирован:")
            print(f"   {guest}")
        except Exception as e:
            print(f"\nОшибка: {e}")
        self._pause()
    
    def book_room_flow(self):
        self._clear_screen()
        print("\nСОЗДАНИЕ БРОНИРОВАНИЯ")
        print("-" * 80)
        
        guest_id = input("  ID гостя (например, G0001): ").strip()
        guest = self.reception.storage.get_guest(guest_id)
        if not guest:
            print(f"\nГость с ID {guest_id} не найден. Сначала зарегистрируйте гостя.")
            self._pause()
            return
        print(f"  Гость: {guest.name}")
        
        available_rooms = self.reception.storage.find_available_rooms(min_berths=1)
        if not available_rooms:
            print("\nНет доступных номеров")
            self._pause()
            return
        
        print("\nДоступные номера:")
        for i, room in enumerate(available_rooms, 1):
            print(f"  {i}. {room}")
        
        try:
            choice = int(input("\n  Выберите номер (цифра): ")) - 1
            if choice < 0 or choice >= len(available_rooms):
                print("\nНеверный выбор")
                self._pause()
                return
            room_number = available_rooms[choice].number
            
            check_in_str = input("  Дата заселения (ДД.ММ.ГГГГ): ").strip()
            check_out_str = input("  Дата выселения (ДД.ММ.ГГГГ): ").strip()
            
            check_in = datetime.strptime(check_in_str, "%d.%m.%Y")
            check_out = datetime.strptime(check_out_str, "%d.%m.%Y")
            
            if check_out <= check_in:
                print("\nДата выселения должна быть позже даты заселения")
                self._pause()
                return
            
            booking = self.reception.book_room(guest_id, room_number, check_in, check_out)
            print(f"\nБронирование успешно создано!")
            print(f"   {booking}")
        except ValueError as e:
            print(f"\nОшибка ввода даты или номера: {e}")
        except HotelException as e:
            # Ловим наши кастомные исключения
            print(f"\nОшибка системы: {e}")
        except Exception as e:
            print(f"\nНеизвестная ошибка: {e}")
        self._pause()
    
    def check_in_flow(self):
        self._clear_screen()
        print("\nЗАСЕЛЕНИЕ ГОСТЯ")
        print("-" * 80)
        booking_id = input("  ID бронирования (например, B0001): ").strip()
        
        try:
            self.reception.check_in_guest(booking_id)
            booking = self.reception.storage.get_booking(booking_id)
            if booking:
                print(f"\nГость {booking.guest.name} заселен в номер {booking.room.number}")
        except HotelException as e:
            print(f"\nОшибка: {e}")
        except Exception as e:
            print(f"\nНеизвестная ошибка: {e}")
        self._pause()
    
    def order_service_flow(self):
        self._clear_screen()
        print("\nЗАКАЗ ДОПОЛНИТЕЛЬНОЙ УСЛУГИ")
        print("-" * 80)
        booking_id = input("  ID бронирования (например, B0001): ").strip()
        
        booking = self.reception.storage.get_booking(booking_id)
        if not booking or booking.status != BookingStatus.CHECKED_IN:
            print("\nНевозможно заказать услугу: гость не заселен или бронь не найдена")
            self._pause()
            return
        
        print(f"  Гость: {booking.guest.name}, Номер: {booking.room.number}")
        print("\nДоступные услуги:")
        services = [
            ("restaurant", "Ресторан"),
            ("spa", "СПА"),
            ("laundry", "Прачечная"),
            ("transfer", "Трансфер")
        ]
        for i, (service_type, name) in enumerate(services, 1):
            print(f"  {i}. {name}")
        
        try:
            choice = int(input("\n  Выберите услугу (цифра): "))
            if choice < 1 or choice > len(services):
                print("\nНеверный выбор")
                self._pause()
                return
            service_type = services[choice - 1][0]
            
            description = input("  Описание услуги: ").strip()
            price = float(input("  Стоимость (BYN): ").strip())
            
            order = self.reception.order_service(booking_id, service_type, description, price)
            print(f"\nУслуга успешно заказана:")
            print(f"   {order}")
        except ValueError as e:
            print(f"\nОшибка ввода: {e}")
        except HotelException as e:
            print(f"\nОшибка системы: {e}")
        except Exception as e:
            print(f"\nНеизвестная ошибка: {e}")
        self._pause()
    
    def check_out_flow(self):
        self._clear_screen()
        print("\nВЫСЕЛЕНИЕ И ОПЛАТА")
        print("-" * 80)
        booking_id = input("  ID бронирования (например, B0001): ").strip()
        
        booking = self.reception.storage.get_booking(booking_id)
        if not booking:
            print("\nБронирование не найдено")
            self._pause()
            return
        
        print(f"\nИнформация о бронировании:")
        print(booking)
        
        try:
            payment = float(input("\n  Сумма оплаты (BYN): ").strip())
            change = self.reception.check_out_guest(booking_id, payment)
            print(f"\nВыселение завершено успешно!")
            print(f"   Итого к оплате: {booking.total_amount:.2f} BYN")
            if change > 0:
                print(f"   Сдача: {change:.2f} BYN")
            else:
                print(f"   Оплачено точно")
        except ValueError as e:
            print(f"\nОшибка ввода: {e}")
        except HotelException as e:
            # Здесь мы красиво выводим наши кастомные ошибки (PaymentError и т.д.)
            print(f"\nОшибка операции: {e}")
        except Exception as e:
            print(f"\nНеизвестная ошибка: {e}")
        self._pause()
    
    def show_statistics(self):
        self._clear_screen()
        rooms = self.reception.get_all_rooms()
        bookings = self.reception.get_active_bookings()
        
        available = len([r for r in rooms if r.status == RoomStatus.AVAILABLE])
        booked = len([r for r in rooms if r.status == RoomStatus.BOOKED])
        occupied = len([r for r in rooms if r.status == RoomStatus.OCCUPIED])
        total = len(rooms)
        
        print("\n" + "="*80)
        print("СТАТИСТИКА ОТЕЛЯ")
        print("="*80)
        print(f"Всего номеров: {total}")
        print(f"  * Свободно:    {available:3d} ({available/total*100:5.1f}%)")
        print(f"  * Забронировано: {booked:3d} ({booked/total*100:5.1f}%)")
        print(f"  * Заселено:    {occupied:3d} ({occupied/total*100:5.1f}%)")
        print(f"\nАктивных бронирований: {len(bookings)}")
        print("="*80)
        self._pause()
    
    def main_menu(self):
        try:
            while self.running:
                self._clear_screen()
                print("\n" + "="*80)
                print("СИСТЕМА УПРАВЛЕНИЯ ОТЕЛЕМ")
                print("="*80)
                print("1. Показать все номера")
                print("2. Показать активные бронирования")
                print("3. Зарегистрировать нового гостя")
                print("4. Забронировать номер")
                print("5. Заселить гостя")
                print("6. Заказать дополнительную услугу")
                print("7. Выселить гостя и оплатить")
                print("8. Статистика отеля")
                print("0. Выйти (данные будут сохранены)")
                print("="*80)
                
                choice = input("\nВыберите действие: ").strip()
                
                if choice == "1":
                    self.display_rooms()
                elif choice == "2":
                    self.display_bookings()
                elif choice == "3":
                    self.register_guest_flow()
                elif choice == "4":
                    self.book_room_flow()
                elif choice == "5":
                    self.check_in_flow()
                elif choice == "6":
                    self.order_service_flow()
                elif choice == "7":
                    self.check_out_flow()
                elif choice == "8":
                    self.show_statistics()
                elif choice == "0":
                    print("\nСохранение данных...")
                    self.reception.save_data()
                    print("\nДо свидания! Спасибо за работу с системой отеля.")
                    self.running = False
                else:
                    print("\nНеверный выбор. Попробуйте снова.")
                    self._pause()
        except KeyboardInterrupt:
            print("\n\nПринудительное сохранение данных...")
            self.reception.save_data()
            print("Программа завершена.")
        except Exception as e:
            print(f"\nКритическая ошибка: {e}")
            import traceback
            traceback.print_exc()
            self._pause()