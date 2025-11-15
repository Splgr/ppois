from typing import Optional
from User import User
from UserRepository import UserRepository
from exceptions import InvalidCredentialsException

class AuthenticationService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
        self._active_sessions: dict[str, User] = {}
    
    def login(self, username: str, password: str) -> User:
        if not self._user_repository.verify_credentials(username, password):
            raise InvalidCredentialsException("Invalid credentials")
        
        user = self._user_repository.find_by_username(username)
        self._active_sessions[user.user_id] = user
        return user
    
    def logout(self, user_id: str) -> None:
        if user_id in self._active_sessions:
            del self._active_sessions[user_id]
    
    def get_current_user(self, user_id: str) -> Optional[User]:
        return self._active_sessions.get(user_id)