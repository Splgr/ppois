from datetime import datetime
from typing import Optional
from student import Student
from course import Course
from exceptions import InsufficientPermissionsException

class Certificate:
    def __init__(self, student: Student, course: Course):
        if course not in student._completed_courses:
            raise InsufficientPermissionsException("Student must complete course to receive certificate")
        
        self._student = student
        self._course = course
        self._issue_date = datetime.now()
        self._grade: Optional[float] = None
    
    def set_grade(self, grade: float) -> None:
        self._grade = grade
    
    def verify_certificate(self) -> bool:
        return (self._student is not None and 
                self._course is not None and 
                self._grade is not None)
    
    def get_certificate_info(self) -> dict:
        return {
            "student": self._student.get_profile_info(),
            "course": self._course.get_course_info(),
            "issue_date": self._issue_date,
            "grade": self._grade
        }