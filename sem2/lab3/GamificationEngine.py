from Student import Student

class GamificationEngine:
    def __init__(self):
        self._points_system: dict[str, int] = {
            "complete_lesson": 10,
            "complete_assignment": 25
        }
        self._student_points: dict[str, int] = {}
    
    def award_points(self, student: Student, action: str) -> int:
        points = self._points_system.get(action, 0)
        if student.user_id not in self._student_points:
            self._student_points[student.user_id] = 0
        self._student_points[student.user_id] += points
        return points
    
    def get_student_points(self, student: Student) -> int:
        return self._student_points.get(student.user_id, 0)
    
    def calculate_student_level(self, student: Student) -> int:
        points = self.get_student_points(student)
        return points // 100 + 1