from typing import List, Dict
from datetime import datetime
from Employee import Employee

class SecuritySystem:
    def __init__(self):
        self._cameras: List[str] = []
        self._access_logs: List[Dict] = []
        self._alarm_status: bool = False
        self._authorized_personnel: List[Employee] = []
        self._incident_reports: List[str] = []

    def log_access(self, employee: Employee, area: str) -> None:
        self._access_logs.append({
            'employee': employee.name,
            'area': area,
            'timestamp': datetime.now()
        })