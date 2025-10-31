from datetime import datetime, timedelta
from typing import Optional
from exceptions import InvalidDrugError

class Drug:
    def __init__(
        self,
        name: str,
        dosage: str,
        price: float,
        batch_code: str,
        storage_conditions: str,
        category: str,
        manufacture_date: Optional[datetime] = None,
        expiration_days: int = 1080
    ):
        if not all([name, dosage, batch_code, category]):
            raise InvalidDrugError("Обязательные поля не заполнены")
        if price < 0:
            raise InvalidDrugError("Цена не может быть отрицательной")

        self.name = name
        self.dosage = dosage
        self.price = price
        self.batch_code = batch_code
        self.storage_conditions = storage_conditions
        self.category = category
        self.manufacture_date = manufacture_date or datetime.now()
        self.expiration_days = expiration_days
        self._expiration_date = self.manufacture_date + timedelta(days=expiration_days)

    @property
    def expiration_date(self) -> datetime:
        return self._expiration_date