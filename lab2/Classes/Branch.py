from typing import List, Optional
from Company import Company
from Manager import Manager
from Employee import Employee

class Branch:
    def __init__(self, location: str, company: Company):
        self.location = location
        self.company = company
        self._manager: Optional['Manager'] = None
        self._sales = 0.0
        self._employees: List['Employee'] = []

    @property
    def manager(self) -> Optional['Manager']:
        return self._manager

    def assign_manager(self, manager: 'Manager') -> None:
        """Назначить менеджера"""
        if self._manager:
            raise Exception("Менеджер уже назначен")
        self._manager = manager
        self._employees.append(manager)

    def add_sale(self, amount: float) -> None:
        """Добавить продажу"""
        if amount <= 0:
            raise Exception("Сумма продажи должна быть положительной")
        self._sales += amount
        self.company.add_revenue(amount)

    def get_sales_report(self) -> dict:
        """Отчет по продажам"""
        return {
            'location': self.location,
            'total_sales': self._sales,
            'manager': self._manager.name if self._manager else 'Не назначен',
            'employee_count': len(self._employees)
        }