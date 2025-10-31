from PrescriptionDrug import PrescriptionDrug
from TestSubject import TestSubject

class Vaccine(PrescriptionDrug):
    def __init__(self, name: str, dosage: str, price: float, batch_code: str, 
                 storage_conditions: str, doses_required: int):
        super().__init__(name, dosage, price, batch_code, storage_conditions, "Вакцина")
        self.doses_required = doses_required
        self._doses_administered = 0

    def administer_dose(self, subject: TestSubject) -> str:
        """Ввести дозу вакцины"""
        if self._doses_administered >= self.doses_required:
            return "Все дозы уже введены"
        
        self._doses_administered += 1
        subject.administer_drug(self, f"Доза вакцины {self._doses_administered}/{self.doses_required}")
        
        if self._doses_administered == self.doses_required:
            subject.vaccinated = True
            subject.immune = min(subject.immune + 3, 10)
            return "Вакцинация завершена"
        
        return f"Введена доза {self._doses_administered} из {self.doses_required}"

    def get_vaccination_progress(self) -> dict:
        return {
            'completed': self._doses_administered >= self.doses_required,
            'doses_administered': self._doses_administered,
            'doses_required': self.doses_required
        }