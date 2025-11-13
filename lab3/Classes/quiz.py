from quiz_question import QuizQuestion
from student import Student
from exceptions import QuizAttemptsExceededException

class Quiz:
    def __init__(self, quiz_id: str, title: str):
        self._quiz_id = quiz_id
        self._title = title
        self._questions: list[QuizQuestion] = []
        self._time_limit_minutes: int = 30
        self._max_attempts: int = 3
        self._attempts: dict[str, int] = {}
    
    def add_question(self, question: QuizQuestion) -> None:
        self._questions.append(question)
    
    def set_time_limit(self, minutes: int) -> None:
        self._time_limit_minutes = minutes
    
    def get_question_count(self) -> int:
        return len(self._questions)
    
    def get_total_points(self) -> float:
        return sum(question._points for question in self._questions)
    
    def can_attempt(self, student: Student) -> bool:
        attempts = self._attempts.get(student.user_id, 0)
        return attempts < self._max_attempts
    
    def record_attempt(self, student: Student) -> None:
        attempts = self._attempts.get(student.user_id, 0)
        if attempts >= self._max_attempts:
            raise QuizAttemptsExceededException("Maximum quiz attempts exceeded")
        self._attempts[student.user_id] = attempts + 1