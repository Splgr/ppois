from user import User
from enums import UserRole, CourseStatus
from exceptions import DuplicateEnrollmentException, CourseNotFoundException, CourseNotPublishedException

class Student(User):
    def __init__(self, user_id: str, username: str, email: str):
        super().__init__(user_id, username, email)
        self._enrolled_courses: list = []
        self._completed_courses: list = []
        self._favorite_courses: set[str] = set()
    
    def get_role(self) -> UserRole:
        return UserRole.STUDENT
    
    def enroll_in_course(self, course) -> None:
        if course._status != CourseStatus.PUBLISHED:
            raise CourseNotPublishedException("Cannot enroll in unpublished course")
        
        if course in self._enrolled_courses:
            raise DuplicateEnrollmentException("Already enrolled in this course")
        
        course.add_student(self)
        self._enrolled_courses.append(course)
    
    def complete_course(self, course) -> None:
        if course not in self._enrolled_courses:
            raise CourseNotFoundException("Course not found in enrolled courses")
        
        self._enrolled_courses.remove(course)
        self._completed_courses.append(course)
    
    def add_to_favorites(self, course) -> None:
        if course not in self._enrolled_courses:
            raise CourseNotFoundException("Cannot favorite a course you're not enrolled in")
        self._favorite_courses.add(course.course_id)
    
    def remove_from_favorites(self, course) -> None:
        self._favorite_courses.discard(course.course_id)
    
    def get_enrollment_count(self) -> int:
        return len(self._enrolled_courses)
    
    def get_completion_count(self) -> int:
        return len(self._completed_courses)