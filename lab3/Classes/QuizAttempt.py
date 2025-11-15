from datetime import datetime
from typing import Optional
from student import Student
from quiz import Quiz
from exceptions import QuizAttemptsExceededException

class QuizAttempt:
    def __init__(self, student: Student, quiz: Quiz):
        if not quiz.can_attempt(student):
            raise QuizAttemptsExceededException("Maximum quiz attempts exceeded")
        
        quiz.record_attempt(student)
        self._student = student
        self._quiz = quiz
        self._start_time = datetime.now()
        self._score: Optional[float] = None
        self._answers: dict[str, str] = {}
    
    def submit_answer(self, question_id: str, answer: str) -> None:
        self._answers[question_id] = answer
    
    def calculate_score(self) -> float:
        total_points = 0
        earned_points = 0
        
        for question in self._quiz._questions:
            total_points += question._points
            student_answer = self._answers.get(question._question_text)
            if student_answer and question.validate_answer(student_answer):
                earned_points += question._points
        
        self._score = (earned_points / total_points * 100) if total_points > 0 else 0
        return self._score