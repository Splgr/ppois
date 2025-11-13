from user import User
from enums import UserRole

class ContentCreator(User):
    def __init__(self, user_id: str, username: str, email: str):
        super().__init__(user_id, username, email)
        self._created_content: list = []
        self._specialization: str = ""
    
    def get_role(self) -> UserRole:
        return UserRole.CONTENT_CREATOR
    
    def create_learning_content(self, content_data: dict):
        from learning_content import LearningContent
        content = LearningContent(content_data['content_id'], content_data['title'], self)
        self._created_content.append(content)
        return content
    
    def set_specialization(self, specialization: str) -> None:
        self._specialization = specialization
    
    def get_content_count(self) -> int:
        return len(self._created_content)