from PrescriptionDrug import PrescriptionDrug
from TestSubject import TestSubject

class Antibiotic(PrescriptionDrug):
    def __init__(self, name: str, dosage: str, price: float, batch_code: str, 
                 storage_conditions: str, spectrum: str):
        super().__init__(name, dosage, price, batch_code, storage_conditions, "Антибиотик")
        self.spectrum = spectrum
        self._resistance_checked = False

    def check_resistance(self, subject: TestSubject) -> str:
        """Проверить резистентность"""
        self._resistance_checked = True
        subject.administer_drug(self, "Проверка резистентности")
        return f"Резистентность к {self.spectrum} проверена"

    def administer(self, subject: TestSubject) -> str:
        """Ввести антибиотик"""
        if not self._resistance_checked:
            return "Сначала проверьте резистентность"
        
        subject.administer_drug(self, "Введение антибиотика")
        subject.immune = min(subject.immune + 2, 10)
        return f"Антибиотик {self.name} введен"