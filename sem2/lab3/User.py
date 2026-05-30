from abc import ABC, abstractmethod
from datetime import datetime
from enums import UserRole

class User(ABC):
    def __init__(self, user_id: str, username: str, email: str):
        self._user_id = user_id
        self._username = username
        self._email = email
        self._registration_date = datetime.now()
        self._is_active = True
        
    @abstractmethod
    def get_role(self) -> UserRole:
        pass
    
    def get_profile_info(self) -> dict:
        return {
            "user_id": self._user_id,
            "username": self._username,
            "email": self._email,
            "role": self.get_role().value
        }
    
    def deactivate_account(self) -> None:
        self._is_active = False
    
    def reactivate_account(self) -> None:
        self._is_active = True
    
    @property
    def user_id(self) -> str:
        return self._user_id
    
    @property
    def username(self) -> str:
        return self._username