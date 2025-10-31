from datetime import datetime
from DrugValidator import DrugValidator
from Drug import Drug
from exceptions import ExpiredDrugError, InvalidDrugError

class SimpleDrugValidator(DrugValidator):
    def validate(self, drug: Drug) -> str:
        if datetime.now() > drug.expiration_date:
            days = (datetime.now() - drug.expiration_date).days
            raise ExpiredDrugError(f"Срок годности истёк {days} дней назад")
        if "холод" in drug.storage_conditions.lower():
            raise InvalidDrugError("Требуется охлаждение")
        days_left = (drug.expiration_date - datetime.now()).days
        return f"Валидно. Осталось {days_left} дней"

    def check_compatibility(self, drug1: Drug, drug2: Drug) -> str:
        return "Совместимо" if drug1.category == drug2.category else "Несовместимо"