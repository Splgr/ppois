from datetime import datetime
from User import User

class ChatMessage:
    def __init__(self, author: User, content: str):
        self._author = author
        self._content = content
        self._timestamp = datetime.now()
    
    def get_message_info(self) -> dict:
        return {
            "author": self._author.username,
            "content": self._content,
            "timestamp": self._timestamp
        }