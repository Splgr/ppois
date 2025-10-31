from Employee import Employee
from CustomerManagerMixin import CustomerManagerMixin
from Order import Order
from datetime import datetime

class Manager(Employee, CustomerManagerMixin):
    def __init__(
        self,
        name: str,
        position: str,
        salary: float,
        employee_id: str,
        hire_date: datetime,
        department: str,
        team_size: int,
        budget: float
    ):
        Employee.__init__(self, name, position, salary, employee_id, hire_date)
        CustomerManagerMixin.__init__(self)
        self.department = department
        self.team_size = team_size
        self.budget = budget

    def approve_order(self, order: Order) -> None:
        if order.status != "Pending":
            raise Exception("Можно утвердить только ожидающий заказ")
        order.approve()
        print(f"Заказ {order.order_id} утвержден менеджером {self.name}")

    def allocate_budget(self, amount: float) -> None:
        if amount > self.budget:
            raise Exception("Недостаточно бюджета")
        self.budget -= amount
        print(f"Бюджет распределён: ${amount}. Остаток: ${self.budget}")

    def attend_training(self) -> None:
        print("Тренинг для менеджеров посещен")
        self.salary += 1000
        print(f"Новая зарплата: {self.salary}")

    def __str__(self) -> str:
        return f"Менеджер {self.name}, отдел: {self.department}, команда: {self.team_size} чел."