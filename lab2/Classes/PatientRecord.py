from datetime import datetime
from typing import List
from Employee import Employee

class PatientRecord:
    def __init__(self, rec_id: str, details: str, patient_name: str):
        self.rec_id = rec_id
        self.details = details
        self.patient_name = patient_name
        self.authorized_employee = None
        self._access_log: List[str] = []

    def update_details(self, new_details: str) -> None:
        """Обновляет детали карты (SRP)"""
        self.details = new_details
        self._access_log.append(f"Обновлено: {datetime.now()}")

    def grant_access(self, employee: 'Employee') -> None:
        """Предоставляет доступ сотруднику"""
        self.authorized_employee = employee
        self._access_log.append(f"Доступ предоставлен {employee.name}: {datetime.now()}")

    def revoke_access(self) -> None:
        """Отзывает доступ"""
        self.authorized_employee = None
        self._access_log.append(f"Доступ отозван: {datetime.now()}")

    def get_access_log(self) -> List[str]:
        """Возвращает лог доступа (неизменяемый)"""
        return self._access_log.copy()