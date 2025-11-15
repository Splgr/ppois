from Course import Course
from Student import Student
from exceptions import StudyGroupFullException, CourseNotFoundException, DuplicateEnrollmentException

class StudyGroup:
    def __init__(self, group_id: str, name: str, course: Course):
        self._group_id = group_id
        self._name = name
        self._course = course
        self._members: list[Student] = []
        self._max_members: int = 10
    
    def add_member(self, student: Student) -> bool:
        if len(self._members) >= self._max_members:
            raise StudyGroupFullException("Study group is full")
        
        if student not in self._course._current_students:
            raise CourseNotFoundException("Student not enrolled in the course")
        
        if student in self._members:
            raise DuplicateEnrollmentException("Student already in study group")
        
        self._members.append(student)
        return True
    
    def remove_member(self, student: Student) -> bool:
        if student in self._members:
            self._members.remove(student)
            return True
        return False
    
    def get_member_count(self) -> int:
        return len(self._members)
    
    def is_full(self) -> bool:
        return len(self._members) >= self._max_members