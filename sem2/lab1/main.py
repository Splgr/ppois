from HotelMenu import HotelMenu
from HotelStorage import HotelStorage
from Reception import Reception

def main():
    print("Добро пожаловать в систему управления отелем!")
    print("Загрузка данных...")
    
    storage = HotelStorage("hotel_data.json")
    reception = Reception(storage)
    menu = HotelMenu(reception)
    menu.main_menu()
    
if __name__ == "__main__":
    main()