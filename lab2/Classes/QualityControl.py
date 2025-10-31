from datetime import datetime
from typing import List, Dict
from Batch import Batch

class QualityControl:
    def __init__(self):
        self._quality_standards: List[str] = []
        self._inspection_reports: List[Dict] = []
        self._defect_rate: float = 0.0
        self._certifications: List[str] = []
        self._last_audit: datetime = datetime.now()

    def perform_inspection(self, batch: Batch) -> bool:
        return datetime.now() < batch.expiry_date