class ServiceType:
    RESTAURANT = "restaurant"
    SPA = "spa"
    LAUNDRY = "laundry"
    TRANSFER = "transfer"
    
    @staticmethod
    def display(service_type: str) -> str:
        mapping = {
            "restaurant": "Ресторан",
            "spa": "СПА",
            "laundry": "Прачечная",
            "transfer": "Трансфер"
        }
        return mapping.get(service_type, service_type)