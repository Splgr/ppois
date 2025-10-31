from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from PasswordValidator import PasswordValidator
from Customer import Customer

class Employee(ABC):
    def __init__(
        self,
        name: str,
        position: str,
        salary: float,
        employee_id: str,
        hire_date: datetime
    ):
        self.name = name
        self.position = position
        self.salary = salary
        self.employee_id = employee_id
        self.hire_date = hire_date

    def check_password(self, password: str, validator: PasswordValidator) -> None:
        if not validator.validate(password):
            raise Exception("Доступ запрещён")
        print(f"Пароль для {self.name} подтвержден")

    @abstractmethod
    def attend_training(self) -> None: 
        pass