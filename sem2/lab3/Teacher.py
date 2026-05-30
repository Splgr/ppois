from User import User
from enums import UserRole

class Teacher(User):
    def __init__(self, user_id: str, username: str, email: str):
        super().__init__(user_id, username, email)
        self._taught_courses: list = []
        self._specializations: list[str] = []
    
    def get_role(self) -> UserRole:
        return UserRole.TEACHER
    
    def create_course(self, course_manager, course_data: dict):
        course = course_manager.create_course(self, course_data)
        self._taught_courses.append(course)
        return course
    
    def add_specialization(self, specialization: str) -> None:
        if specialization not in self._specializations:
            self._specializations.append(specialization)
    
    def get_specializations(self) -> list[str]:
        return self._specializations.copy()
    
    def get_total_students_taught(self) -> int:
        return sum(len(course._current_students) for course in self._taught_courses)