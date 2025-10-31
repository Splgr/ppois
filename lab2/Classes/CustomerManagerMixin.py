from typing import List
from Customer import Customer

class CustomerManagerMixin:
    def __init__(self):
        self.managed_customers: List[Customer] = []

    def assign_customer(self, customer: Customer) -> None:
        self.managed_customers.append(customer)
        print(f"Клиент {customer.name} назначен {getattr(self, 'name', 'сотруднику')}")