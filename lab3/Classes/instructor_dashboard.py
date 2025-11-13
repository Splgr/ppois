from teacher import Teacher
from course import Course
from exceptions import InsufficientPermissionsException

class InstructorDashboard:
    def __init__(self, instructor: Teacher):
        self._instructor = instructor
        self._course_metrics: dict[str, dict] = {}
    
    def update_course_metrics(self, course: Course) -> None:
        if course._instructor != self._instructor:
            raise InsufficientPermissionsException("Instructor can only access their own courses")
        
        metrics = {
            "total_students": len(course._current_students),
            "completion_rate": 75.0,
            "avg_grade": 82.5
        }
        self._course_metrics[course.course_id] = metrics
    
    def get_teaching_insights(self) -> dict[str, any]:
        return {
            "most_popular_course": "Python Basics",
            "total_students": self._instructor.get_total_students_taught()
        }