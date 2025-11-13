from enum import Enum

class UserRole(Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"
    CONTENT_CREATOR = "content_creator"

class CourseStatus(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"