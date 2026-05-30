from core import storage, reception
from core.models import hotel_menu

if __name__ == "__main__":
    storage = storage("data/hotel_data.json")
    reception = reception(storage)
    menu = hotel_menu(reception)
    menu.main_menu()