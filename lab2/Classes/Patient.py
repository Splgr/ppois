from typing import List
from Prescription import Prescription

class Patient:
    def __init__(self, name: str, age: int, medical_history: str):
        if age < 0 or age > 150:
            raise Exception("Некорректный возраст")
        
        self.name = name
        self.age = age
        self.medical_history = medical_history
        self.prescriptions: List[Prescription] = []
        self._allergies: List[str] = []

    def add_prescription(self, prescription: Prescription) -> None:
        """Добавляет рецепт (SRP)"""
        self.prescriptions.append(prescription)

    def add_allergy(self, allergy: str) -> None:
        """Добавляет аллергию"""
        self._allergies.append(allergy.lower())

    def has_allergy_to(self, drug_category: str) -> bool:
        """Проверяет наличие аллергии на категорию лекарств"""
        return any(allergy in drug_category.lower() for allergy in self._allergies)

    def get_active_prescriptions(self) -> List[Prescription]:
        """Возвращает активные рецепты"""
        return [p for p in self.prescriptions if not p.is_used]