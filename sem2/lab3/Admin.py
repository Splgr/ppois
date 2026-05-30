from User import User
from enums import UserRole
from UserRepository import UserRepository

class Admin(User):
    def __init__(self, user_id: str, username: str, email: str):
        super().__init__(user_id, username, email)
    
    def get_role(self) -> UserRole:
        return UserRole.ADMIN
    
    def suspend_user(self, user_repository: UserRepository, user_id: str) -> None:
        user = user_repository.find_by_id(user_id)
        user.deactivate_account()
    
    def unsuspend_user(self, user_repository: UserRepository, user_id: str) -> None:
        user = user_repository.find_by_id(user_id)
        user.reactivate_account()