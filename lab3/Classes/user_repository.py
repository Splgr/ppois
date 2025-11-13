from user import User
from exceptions import UserNotFoundException

class UserRepository:
    def __init__(self):
        self._users: dict[str, User] = {}
        self._user_credentials: dict[str, str] = {}
    
    def add_user(self, user: User, password: str) -> None:
        self._users[user.user_id] = user
        self._user_credentials[user.username] = password
    
    def find_by_id(self, user_id: str) -> User:
        user = self._users.get(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found")
        return user
    
    def find_by_username(self, username: str) -> User:
        for user in self._users.values():
            if user.username == username:
                return user
        raise UserNotFoundException(f"User with username {username} not found")
    
    def verify_credentials(self, username: str, password: str) -> bool:
        stored_password = self._user_credentials.get(username)
        return stored_password == password
    
    def get_total_users_count(self) -> int:
        return len(self._users)