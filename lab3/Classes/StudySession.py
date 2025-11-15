from datetime import datetime
from StudyGroup import StudyGroup
from Student import Student
from exceptions import StudyGroupNotFoundException

class StudySession:
    def __init__(self, study_group: StudyGroup, title: str):
        self._study_group = study_group
        self._title = title
        self._attendees: list[Student] = []
        self._scheduled_time: datetime = datetime.now()
    
    def mark_attendance(self, student: Student) -> None:
        if student not in self._study_group._members:
            raise StudyGroupNotFoundException("Student not in study group")
        
        if student not in self._attendees:
            self._attendees.append(student)
    
    def get_attendance_count(self) -> int:
        return len(self._attendees)
    
    def get_attendance_rate(self) -> float:
        total_members = len(self._study_group._members)
        return (len(self._attendees) / total_members * 100) if total_members > 0 else 0