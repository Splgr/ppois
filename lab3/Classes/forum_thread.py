from datetime import datetime
from typing import Optional
from user import User
from forum_post import ForumPost

class ForumThread:
    def __init__(self, author: User, title: str):
        self._author = author
        self._title = title
        self._creation_date = datetime.now()
        self._posts: list[ForumPost] = []
        self._is_locked: bool = False
        self._view_count: int = 0
    
    def add_post(self, author: User, content: str) -> Optional[ForumPost]:
        if not self._is_locked:
            post = ForumPost(author, content)
            self._posts.append(post)
            return post
        return None
    
    def lock_thread(self) -> None:
        self._is_locked = True
    
    def unlock_thread(self) -> None:
        self._is_locked = False
    
    def increment_view_count(self) -> None:
        self._view_count += 1
    
    def get_post_count(self) -> int:
        return len(self._posts)