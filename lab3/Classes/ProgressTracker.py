from student import Student
from Course import Course
from Lesson import Lesson
from exceptions import CourseNotFoundException

class ProgressTracker:
    def __init__(self, student: Student, course: Course):
        if course not in student._enrolled_courses:
            raise CourseNotFoundException("Student not enrolled in this course")
        
        self._student = student
        self._course = course
        self._completed_lessons: set[str] = set()
        self._time_spent_minutes: int = 0
    
    def mark_lesson_completed(self, lesson: Lesson) -> None:
        self._completed_lessons.add(lesson._lesson_id)
    
    def add_study_time(self, minutes: int) -> None:
        self._time_spent_minutes += minutes
    
    def get_completion_percentage(self, total_lessons: int) -> float:
        return (len(self._completed_lessons) / total_lessons * 100) if total_lessons > 0 else 0
    
    def get_time_spent(self) -> int:
        return self._time_spent_minutes