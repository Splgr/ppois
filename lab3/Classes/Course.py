from enums import CourseStatus
from student import Student
from exceptions import CourseFullException, DuplicateEnrollmentException, CourseNotPublishedException

class Course:
    def __init__(self, course_id: str, title: str, instructor, max_students: int = 100):
        self._course_id = course_id
        self._title = title
        self._instructor = instructor
        self._current_students: list[Student] = []
        self._status = CourseStatus.DRAFT
        self._tags: list[str] = []
        self._difficulty_level: str = "beginner"
        self._max_students = max_students
    
    def add_student(self, student: Student) -> None:
        if len(self._current_students) >= self._max_students:
            raise CourseFullException("Course is full")
        
        elif student in self._current_students:
            raise DuplicateEnrollmentException("Student already enrolled")
        
        elif self._status != CourseStatus.PUBLISHED:
            raise CourseNotPublishedException("Cannot enroll in unpublished course")
        
        else:
            self._current_students.append(student)
    
    def remove_student(self, student: Student) -> None:
        if student in self._current_students:
            self._current_students.remove(student)
    
    def publish(self) -> None:
        self._status = CourseStatus.PUBLISHED
    
    def archive(self) -> None:
        self._status = CourseStatus.ARCHIVED
    
    def add_tag(self, tag: str) -> None:
        if tag not in self._tags:
            self._tags.append(tag)
    
    def get_enrollment_count(self) -> int:
        return len(self._current_students)
    
    def get_course_info(self) -> dict:
        return {
            "course_id": self._course_id,
            "title": self._title,
            "instructor": self._instructor.get_profile_info(),
            "students_count": len(self._current_students),
            "status": self._status.value
        }
    
    @property
    def course_id(self) -> str:
        return self._course_id
    
    @property
    def title(self) -> str:
        return self._title