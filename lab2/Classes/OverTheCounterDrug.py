from Drug import Drug
from datetime import timedelta
from exceptions import InvalidDrugError

class OverTheCounterDrug(Drug):
    def __init__(
        self, name, dosage, price, batch_code, storage_conditions, category,
        manufacture_date=None, expiration_days=1080
    ):
        super().__init__(name, dosage, price, batch_code, storage_conditions, category,
                         manufacture_date, expiration_days)
        self.requires_prescription = False

    def extend_shelf_life(self, days: int) -> None:
        if days <= 0:
            raise InvalidDrugError("Дни должны быть положительными")
        self._expiration_date += timedelta(days=days)

    def recommend_alternative(self, name: str, category: str) -> str:
        if self.name != name and self.category == category:
            return f"Рекомендуем другие препараты категории '{category}'"
        return "Альтернативы не найдены"