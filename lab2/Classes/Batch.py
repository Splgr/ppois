from datetime import datetime, timedelta
from typing import List
from Drug import Drug
from exceptions import BatchRecallError, ExpiredDrugError

class Batch:
    def __init__(self, batch_id: str, production_date: datetime):
        if production_date > datetime.now():
            raise Exception("Дата производства не может быть в будущем")
        
        self.batch_id = batch_id
        self.production_date = production_date
        self.expiry_date = production_date + timedelta(days=1080)  # 3 года
        self._drugs: List[Drug] = []
        self._is_recalled = False

    def add_drug(self, drug: Drug) -> None:
        """Добавить лекарство в партию"""
        if self._is_recalled:
            raise BatchRecallError("Нельзя добавить лекарство в отозванную партию")
        self._drugs.append(drug)

    def recall(self) -> None:
        """Отозвать партию"""
        self._is_recalled = True
        raise BatchRecallError(f"Партия {self.batch_id} отозвана")

    def inspect_quality(self) -> str:
        """Проверить качество партии"""
        if self._is_recalled:
            return "Партия отозвана"
        
        if datetime.now() > self.expiry_date:
            raise ExpiredDrugError("Партия просрочена")
        
        return f"Партия {self.batch_id} в хорошем состоянии, лекарств: {len(self._drugs)}"

    def get_drug_count(self) -> int:
        return len(self._drugs)