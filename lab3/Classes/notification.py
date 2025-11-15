from datetime import datetime
from User import User

class Notification:
    def __init__(self, user: User, title: str):
        self._user = user
        self._title = title
        self._sent_date = datetime.now()
        self._is_read: bool = False
    
    def mark_as_read(self) -> None:
        self._is_read = True
    
    def mark_as_unread(self) -> None:
        self._is_read = False