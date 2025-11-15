from datetime import datetime
from LearningContent import LearningContent
from User import User

class ContentVersion:
    def __init__(self, content: LearningContent, author: User):
        self._content = content
        self._author = author
        self._created_date = datetime.now()
        self._is_current: bool = False
    
    def make_current(self) -> None:
        self._is_current = True
    
    def get_version_info(self) -> dict:
        return {
            "author": self._author.get_profile_info(),
            "created_date": self._created_date,
            "is_current": self._is_current
        }