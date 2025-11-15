from datetime import datetime
from typing import Optional
from student import Student
from Course import Course
from exceptions import CourseNotFoundException

class StudyReminder:
    def __init__(self, reminder_id: str, student: Student, title: str, reminder_time: datetime):
        self._reminder_id = reminder_id
        self._student = student
        self._title = title
        self._reminder_time = reminder_time
        self._is_completed = False
        self._course: Optional[Course] = None
    
    def set_course(self, course: Course) -> None:
        if course not in self._student._enrolled_courses:
            raise CourseNotFoundException("Student not enrolled in this course")
        self._course = course
    
    def mark_completed(self) -> None:
        self._is_completed = True
    
    def mark_incomplete(self) -> None:
        self._is_completed = False
    
    def is_due(self) -> bool:
        return datetime.now() >= self._reminder_time and not self._is_completed
    
    def get_reminder_info(self) -> dict:
        return {
            "reminder_id": self._reminder_id,
            "title": self._title,
            "reminder_time": self._reminder_time,
            "is_completed": self._is_completed,
            "course": self._course.title if self._course else None,
            "is_due": self.is_due()
        }
    
    def reschedule(self, new_time: datetime) -> None:
        self._reminder_time = new_time