from typing import List
from Customer import Customer

class LoyaltyProgram:
    def __init__(self, program_name: str, points_per_purchase: int, discount_percentage: float):
        self.program_name = program_name
        self.points_per_purchase = points_per_purchase
        self.discount_percentage = discount_percentage
        self._members: List[Customer] = []
        self._total_points_issued = 0
        self._active_campaigns: List[str] = []

    def enroll_customer(self, customer: Customer) -> None:
        self._members.append(customer)

    def calculate_reward(self, points: int) -> float:
        return points * (self.discount_percentage / 100)