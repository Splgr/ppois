from Course import Course
from Student import Student
from exceptions import CourseNotFoundException

class LearningPath:
    def __init__(self, path_id: str, title: str):
        self._path_id = path_id
        self._title = title
        self._courses: list[Course] = []
        self._description: str = ""
    
    def add_course(self, course: Course) -> None:
        self._courses.append(course)
    
    def set_description(self, description: str) -> None:
        self._description = description
    
    def enroll_student(self, student: Student) -> bool:
        if not self._courses:
            raise CourseNotFoundException("No courses in learning path")
        
        student.enroll_in_course(self._courses[0])
        return True
    
    def calculate_progress(self, student: Student) -> float:
        completed = sum(1 for course in self._courses if course in student._completed_courses)
        return (completed / len(self._courses)) * 100 if self._courses else 0