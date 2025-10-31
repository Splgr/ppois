from datetime import datetime
from typing import List
from Drug import Drug

class TestSubject:
    def __init__(self, subject_id: str):
        self.subject_id = subject_id
        self.health = 5
        self.vitamins = 5
        self.immune = 5
        self.pain = False
        self.vaccinated = False
        self.alive = True
        self._medical_history: List[str] = []

    def administer_drug(self, drug: Drug, effect: str) -> None:
        """Ввести лекарство и записать эффект"""
        if not self.alive:
            raise Exception("Нельзя вводить лекарство умершему субъекту")
        
        self._medical_history.append(f"{datetime.now()}: {drug.name} - {effect}")
        
        if "обезболивающее" in drug.category.lower():
            self.pain = False
        elif "витамин" in drug.category.lower():
            self.vitamins = min(self.vitamins + 1, 10)

    def check_vital_signs(self) -> dict:
        """Проверить жизненные показатели"""
        if self.health <= 0 or self.immune <= 0:
            self.alive = False
        
        return {
            'alive': self.alive,
            'health': self.health,
            'immune': self.immune,
            'vitamins': self.vitamins,
            'pain': self.pain,
            'vaccinated': self.vaccinated
        }

    def get_medical_history(self) -> List[str]:
        return self._medical_history.copy()