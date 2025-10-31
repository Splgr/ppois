from typing import List
from enums import Status
from Drug import Drug

class Supplier:
    def __init__(
        self,
        name: str,
        contact: str,
        rating: float,
        contract_status: Status,
        supply_frequency: str,
        performance_evaluator = None
    ):
        self.name = name
        self.contact = contact
        self.rating = rating
        self.contract_status = contract_status
        self.supply_frequency = supply_frequency
        self.drugs_supplied: List[Drug] = []
        self._performance_evaluator = performance_evaluator

    def add_drug(self, drug: Drug) -> None:
        self.drugs_supplied.append(drug)
        print(f"Лекарство {drug.name} добавлено к поставщику {self.name}")

    def negotiate_terms(self) -> None:
        if self.contract_status == Status.ACTIVE and self.rating >= 4:
            print(f"Условия согласованы с поставщиком {self.name}")

    def evaluate_performance(self) -> bool:
        return self._performance_evaluator.evaluate(self)

    def __str__(self) -> str:
        return f"Поставщик {self.name}, рейтинг: {self.rating}, статус: {self.contract_status.value}"