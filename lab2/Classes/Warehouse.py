from typing import List, Dict
from datetime import datetime
from Stock import Stock
from Drug import Drug

class Warehouse:
    def __init__(self, warehouse_id: str, total_capacity: int, temperature_control: bool):
        self.warehouse_id = warehouse_id
        self.total_capacity = total_capacity
        self.temperature_control = temperature_control
        self._current_stock: List[Stock] = []
        self._shelves: Dict[str, List[Drug]] = {}
        self._security_level: int = 1
        self._last_inspection: datetime = datetime.now()