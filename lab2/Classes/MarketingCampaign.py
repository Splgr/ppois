from datetime import datetime, timedelta
from typing import List

class MarketingCampaign:
    def __init__(self, campaign_name: str, budget: float, target_audience: str):
        self.campaign_name = campaign_name
        self.budget = budget
        self.target_audience = target_audience
        self._channels: List[str] = []
        self._start_date: datetime = datetime.now()
        self._end_date: datetime = datetime.now() + timedelta(days=30)
        self._conversion_rate: float = 0.0

    def calculate_roi(self) -> float:
        return (self.budget * self._conversion_rate) / self.budget