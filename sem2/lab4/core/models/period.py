from datetime import datetime

class Period:
    """Период проживания"""
    def __init__(self, start: datetime, end: datetime):
        self.start = start
        self.end = end
    
    @property
    def duration_days(self) -> int:
        return max(1, (self.end - self.start).days)
    
    def to_dict(self) -> dict:
        return {"start": self.start.isoformat(), "end": self.end.isoformat()}
    
    @staticmethod
    def from_dict(data: dict) -> 'Period':
        return Period(
            start=datetime.fromisoformat(data["start"]),
            end=datetime.fromisoformat(data["end"])
        )