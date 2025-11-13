from datetime import datetime

class CourseSchedule:
    def __init__(self, course): 
        self._course = course
        self._lessons_schedule: dict[object, datetime] = {}
        self._assignments_deadlines: dict[object, datetime] = {}
    
    def schedule_lesson(self, lesson, date_time: datetime) -> None: 
        self._lessons_schedule[lesson] = date_time
    
    def add_assignment_deadline(self, assignment, deadline: datetime) -> None:
        self._assignments_deadlines[assignment] = deadline
    
    def get_upcoming_events(self, days: int = 7) -> list[dict]:
        upcoming = []
        now = datetime.now()
        
        for lesson, lesson_time in self._lessons_schedule.items():
            if hasattr(lesson, '_title') and 0 <= (lesson_time - now).days <= days:
                upcoming.append({"type": "lesson", "title": lesson._title, "time": lesson_time})
        
        for assignment, deadline in self._assignments_deadlines.items():
            if hasattr(assignment, '_title') and 0 <= (deadline - now).days <= days:
                upcoming.append({"type": "assignment", "title": assignment._title, "deadline": deadline})
        
        return sorted(upcoming, key=lambda x: x['time'] if 'time' in x else x['deadline'])