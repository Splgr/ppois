from User import User
from Achievement import Achievement
from UserAchievement import UserAchievement
from exceptions import AchievementAlreadyAwardedException

class AchievementSystem:
    def __init__(self):
        self._achievements: list[Achievement] = []
        self._user_achievements: dict[str, list[UserAchievement]] = {}
    
    def create_achievement(self, name: str) -> Achievement:
        achievement = Achievement(name)
        self._achievements.append(achievement)
        return achievement
    
    def award_achievement(self, user: User, achievement: Achievement) -> UserAchievement:
        user_achievements = self._user_achievements.get(user.user_id, [])
        for ua in user_achievements:
            if ua._achievement._name == achievement._name:
                raise AchievementAlreadyAwardedException("Achievement already awarded to user")
        
        user_achievement = UserAchievement(user, achievement)
        
        if user.user_id not in self._user_achievements:
            self._user_achievements[user.user_id] = []
        self._user_achievements[user.user_id].append(user_achievement)
        
        return user_achievement
    
    def get_user_achievements(self, user: User) -> list[UserAchievement]:  # Заменили List
        return self._user_achievements.get(user.user_id, [])