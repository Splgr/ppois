from typing import List
from datetime import datetime
from Drug import Drug
from Employee import Employee

class Company:
    def __init__(self, name: str, founded_year: int):
        current_year = datetime.now().year
        if founded_year > current_year:
            raise Exception("Год основания не может быть в будущем")
        
        self.name = name
        self.founded_year = founded_year
        self._revenue = 0.0
        self._employees: List['Employee'] = []
        self._products: List[Drug] = []

    @property
    def revenue(self) -> float:
        return self._revenue

    def add_revenue(self, amount: float) -> None:
        """Добавляет выручку"""
        if amount < 0:
            raise Exception("Выручка не может быть отрицательной")
        self._revenue += amount

    def hire_employee(self, employee: 'Employee') -> None:
        """Нанять сотрудника"""
        if employee in self._employees:
            raise Exception("Сотрудник уже работает в компании")
        self._employees.append(employee)

    def launch_product(self, drug: Drug) -> None:
        """Запустить продукт"""
        self._products.append(drug)
        print(f"Продукт {drug.name} запущен компанией {self.name}")

    def calculate_profit(self, expenses: float) -> float:
        """Рассчитать прибыль"""
        if expenses < 0:
            raise Exception("Расходы не могут быть отрицательными")
        return self._revenue - expenses

    def get_employee_count(self) -> int:
        return len(self._employees)