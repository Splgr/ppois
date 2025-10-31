from OverTheCounterDrug import OverTheCounterDrug
from TestSubject import TestSubject

class Painkiller(OverTheCounterDrug):
    def __init__(self, name: str, dosage: str, price: float, batch_code: str, 
                 storage_conditions: str, strength: str):
        super().__init__(name, dosage, price, batch_code, storage_conditions, "Обезболивающее")
        self.strength = strength

    def relieve_pain(self, subject: TestSubject) -> str:
        """Снять боль"""
        subject.administer_drug(self, "Обезболивание")
        subject.pain = False
        return f"Боль снята с помощью {self.strength} обезболивающего"