from Drug import Drug
from exceptions import InvalidDrugError

class DrugPricingService:
    def apply_discount(self, drug: Drug, percent: float) -> None:
        if not 0 <= percent <= 100:
            raise InvalidDrugError("Скидка должна быть от 0 до 100%")
        drug.price = round(drug.price * (1 - percent / 100), 2)

    def calculate_tax(self, drug: Drug, tax_rate: float) -> float:
        return round(drug.price * (tax_rate / 100), 2)