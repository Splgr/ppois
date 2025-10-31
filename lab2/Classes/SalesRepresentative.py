from Employee import Employee
from CustomerManagerMixin import CustomerManagerMixin
from datetime import datetime

class SalesRepresentative(Employee, CustomerManagerMixin):
    def __init__(
        self,
        name: str,
        position: str,
        salary: float,
        employee_id: str,
        hire_date: datetime,
        sales_quota: float
    ):
        Employee.__init__(self, name, position, salary, employee_id, hire_date)
        CustomerManagerMixin.__init__(self)
        self.sales_quota = sales_quota

    def attend_training(self) -> None:
        print("Тренинг по продажам посещен")
        self.salary += 500
        print(f"Новая зарплата: {self.salary}")

    def __str__(self) -> str:
        return f"Продавец {self.name}, квота: {self.sales_quota}₽"