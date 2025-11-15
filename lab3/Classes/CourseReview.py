from datetime import datetime
from Course import Course
from student import Student
from exceptions import InsufficientPermissionsException, InvalidRatingException

class CourseReview:
    def __init__(self, review_id: str, course: Course, student: Student, rating: float, comment: str):
        if course not in student._completed_courses:
            raise InsufficientPermissionsException("Student must complete course to review it")
        
        if not (1 <= rating <= 5):
            raise InvalidRatingException("Rating must be between 1 and 5")
        
        self._review_id = review_id
        self._course = course
        self._student = student
        self._rating = rating
        self._comment = comment
        self._created_date = datetime.now()
        self._is_verified = False
        self._helpful_count = 0
    
    def verify_review(self) -> None:
        self._is_verified = True
    
    def mark_helpful(self) -> None:
        self._helpful_count += 1
    
    def update_rating(self, new_rating: float) -> None:
        if not (1 <= new_rating <= 5):
            raise InvalidRatingException("Rating must be between 1 and 5")
        self._rating = new_rating
    
    def update_comment(self, new_comment: str) -> None:
        self._comment = new_comment
    
    def get_review_info(self) -> dict:
        return {
            "review_id": self._review_id,
            "course": self._course.title,
            "student": self._student.username,
            "rating": self._rating,
            "comment": self._comment,
            "created_date": self._created_date,
            "is_verified": self._is_verified,
            "helpful_count": self._helpful_count
        }
    
    def is_positive(self) -> bool:
        return self._rating >= 4.0
    
    def is_recent(self, days: int = 30) -> bool:
        return (datetime.now() - self._created_date).days <= days