from datetime import datetime
from typing import Optional
from exceptions import AssignmentDeadlinePassedException

class Assignment:
    def __init__(self, assignment_id: str, title: str):
        self._assignment_id = assignment_id
        self._title = title
        self._submissions: dict[str, ] = {}
        self._max_score: float = 100.0
        self._due_date: Optional[datetime] = None
    
    def submit_assignment(self, student, submission_data: str):
        if self._due_date and datetime.now() > self._due_date:
            raise AssignmentDeadlinePassedException("Assignment deadline has passed")
        
        from assignment_submission import AssignmentSubmission  
        submission = AssignmentSubmission(student, self, submission_data)
        self._submissions[student.user_id] = submission
        return submission
    
    def set_due_date(self, due_date: datetime) -> None:
        self._due_date = due_date
    
    def is_overdue(self) -> bool:
        return self._due_date and datetime.now() > self._due_date
    
    def get_submission_count(self) -> int:
        return len(self._submissions)
    
    def grade_submission(self, student_id: str, grade: float) -> bool:
        if student_id in self._submissions:
            self._submissions[student_id].grade(grade)
            return True
        return False