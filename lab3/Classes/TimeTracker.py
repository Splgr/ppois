from datetime import datetime
from Student import Student
from Course import Course
from StudySessionRecord import StudySessionRecord
from exceptions import CourseNotFoundException

class TimeTracker:
    def __init__(self, student: Student):
        self._student = student
        self._study_sessions: list[StudySessionRecord] = []
        self._daily_goals: dict[str, int] = {}
    
    def start_study_session(self, course: Course) -> None:
        if course not in self._student._enrolled_courses:
            raise CourseNotFoundException("Student not enrolled in this course")
        
        session = StudySessionRecord(course)
        self._study_sessions.append(session)
    
    def set_daily_goal(self, minutes: int) -> None:
        today_str = datetime.now().strftime("%Y-%m-%d")
        self._daily_goals[today_str] = minutes
    
    def get_todays_study_time(self) -> int:
        today = datetime.now().date()
        todays_sessions = [s for s in self._study_sessions if s._end_time and s._end_time.date() == today]
        return sum(session.get_duration_minutes() for session in todays_sessions)
    
    def is_goal_achieved(self) -> bool:
        return self.get_todays_study_time() >= self._daily_goals.get(datetime.now().strftime("%Y-%m-%d"), 0)