from student import Student
from Course import Course
from exceptions import CourseNotFoundException

class StudentPerformanceAnalytics:
    def __init__(self, student: Student):
        self._student = student
        self._course_performance: dict[str, dict[str, float]] = {}
    
    def analyze_course_performance(self, course: Course) -> dict[str, float]:
        if course not in self._student._enrolled_courses:
            raise CourseNotFoundException("Student not enrolled in this course")
        
        performance = {
            "assignments_avg": 85.0,
            "quizzes_avg": 78.0,
            "overall_score": 81.5
        }
        self._course_performance[course.course_id] = performance
        return performance
    
    def predict_final_grade(self, course: Course) -> float:
        performance = self._course_performance.get(course.course_id, {})
        return performance.get("overall_score", 70)