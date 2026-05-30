from datetime import datetime
from User import User
from Achievement import Achievement

class UserAchievement:
    def __init__(self, user: User, achievement: Achievement):
        self._user = user
        self._achievement = achievement
        self._awarded_date = datetime.now()
    
    def get_days_since_awarded(self) -> int:
        return (datetime.now() - self._awarded_date).days