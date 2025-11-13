from datetime import datetime
from teacher import Teacher
from student import Student

class LiveSession:
    def __init__(self, session_id: str, title: str, instructor: Teacher):
        self._session_id = session_id
        self._title = title
        self._instructor = instructor
        self._participants: list[Student] = []
        self._scheduled_time: datetime = datetime.now()
        self._is_active: bool = False
    
    def start_session(self) -> None:
        self._is_active = True
    
    def end_session(self) -> None:
        self._is_active = False
    
    def join_session(self, student: Student) -> None:
        if student not in self._participants:
            self._participants.append(student)
    
    def get_participant_count(self) -> int:
        return len(self._participants)
    
    def is_ongoing(self) -> bool:
        return self._is_active