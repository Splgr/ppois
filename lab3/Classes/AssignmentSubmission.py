from datetime import datetime
from typing import Optional
from student import Student

class AssignmentSubmission:
    def __init__(self, student: Student, assignment, content: str):
        self._student = student
        self._assignment = assignment
        self._content = content
        self._submission_date = datetime.now()
        self._grade: Optional[float] = None
        self._is_graded: bool = False
    
    def grade(self, grade: float) -> None:
        if grade <= self._assignment._max_score:
            self._grade = grade
            self._is_graded = True
    
    def get_grade(self) -> Optional[float]:
        return self._grade
    
    def is_late(self) -> bool:
        return self._assignment._due_date and self._submission_date > self._assignment._due_date