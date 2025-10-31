from datetime import datetime
from typing import Dict, List
from Drug import Drug

class SalesAnalytics:
    def __init__(self):
        self._daily_sales: Dict[datetime, float] = {}
        self._top_products: List[Drug] = []
        self._customer_demographics: Dict[str, int] = {}
        self._monthly_revenue: float = 0.0
        self._sales_target: float = 100000.0

    def add_sale(self, date: datetime, amount: float) -> None:
        self._daily_sales[date] = amount

    def calculate_growth_rate(self) -> float:
        return (self._monthly_revenue / self._sales_target) * 100