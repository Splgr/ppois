from LearningContent import LearningContent
from content_version import ContentVersion
from User import User
from enums import UserRole
from exceptions import InsufficientPermissionsException

class ContentManagementSystem:
    def __init__(self):
        self._content_versions: dict[str, list[ContentVersion]] = {}
        self._approval_queue: list[LearningContent] = []
    
    def create_content_version(self, content: LearningContent, author: User) -> ContentVersion:
        if author.get_role() not in [UserRole.TEACHER, UserRole.CONTENT_CREATOR, UserRole.ADMIN]:
            raise InsufficientPermissionsException("Only teachers, content creators and admins can create content")
        
        version = ContentVersion(content, author)
        
        if content._content_id not in self._content_versions:
            self._content_versions[content._content_id] = []
        self._content_versions[content._content_id].append(version)
        
        self._approval_queue.append(content)
        return version
    
    def approve_content(self, content: LearningContent) -> None:
        if content in self._approval_queue:
            self._approval_queue.remove(content)
            content.approve_content()
    
    def get_pending_approvals(self) -> list[LearningContent]:
        return self._approval_queue.copy()