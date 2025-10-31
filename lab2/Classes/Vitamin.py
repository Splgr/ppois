from OverTheCounterDrug import OverTheCounterDrug
from TestSubject import TestSubject

class Vitamin(OverTheCounterDrug):
    def __init__(self, name: str, dosage: str, price: float, batch_code: str, 
                 storage_conditions: str, vitamin_type: str):
        super().__init__(name, dosage, price, batch_code, storage_conditions, "Витамин")
        self.vitamin_type = vitamin_type

    def boost_health(self, subject: TestSubject) -> str:
        """Улучшить здоровье"""
        subject.administer_drug(self, "Улучшение здоровья")
        subject.health = min(subject.health + 1, 10)
        subject.vitamins = min(subject.vitamins + 1, 10)
        return f"Здоровье улучшено витамином {self.vitamin_type}"