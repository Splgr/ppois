from datetime import datetime
from User import User

class ForumPost:
    def __init__(self, author: User, content: str):
        self._author = author
        self._content = content
        self._post_date = datetime.now()
        self._likes: set[str] = set()
    
    def like(self, user: User) -> None:
        self._likes.add(user.user_id)
    
    def unlike(self, user: User) -> None:
        self._likes.discard(user.user_id)
    
    def get_like_count(self) -> int:
        return len(self._likes)