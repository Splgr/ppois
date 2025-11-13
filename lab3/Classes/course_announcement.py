from datetime import datetime
from course import Course
from user import User
from enums import UserRole
from exceptions import InsufficientPermissionsException

class CourseAnnouncement:
    def __init__(self, announcement_id: str, course: Course, author: User, title: str, content: str):
        if author.get_role() not in [UserRole.TEACHER, UserRole.ADMIN]:
            raise InsufficientPermissionsException("Only teachers and admins can create announcements")
        
        self._announcement_id = announcement_id
        self._course = course
        self._author = author
        self._title = title
        self._content = content
        self._created_date = datetime.now()
        self._is_pinned = False
        self._view_count = 0
    
    def pin_announcement(self) -> None:
        self._is_pinned = True
    
    def unpin_announcement(self) -> None:
        self._is_pinned = False
    
    def increment_view_count(self) -> None:
        self._view_count += 1
    
    def get_announcement_info(self) -> dict:
        return {
            "announcement_id": self._announcement_id,
            "course": self._course.title,
            "author": self._author.username,
            "title": self._title,
            "created_date": self._created_date,
            "is_pinned": self._is_pinned,
            "view_count": self._view_count
        }
    
    def is_recent(self, hours: int = 24) -> bool:
        return (datetime.now() - self._created_date).total_seconds() < hours * 3600