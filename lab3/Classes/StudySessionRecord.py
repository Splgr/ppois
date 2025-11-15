from datetime import datetime
from typing import Optional
from Course import Course

class StudySessionRecord:
    def __init__(self, course: Course):
        self._course = course
        self._start_time = datetime.now()
        self._end_time: Optional[datetime] = None
    
    def end_session(self) -> None:
        self._end_time = datetime.now()
    
    def get_duration_minutes(self) -> int:
        if self._end_time:
            return int((self._end_time - self._start_time).total_seconds() / 60)
        return int((datetime.now() - self._start_time).total_seconds() / 60)