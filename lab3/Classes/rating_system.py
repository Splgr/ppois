from course import Course
from teacher import Teacher
from exceptions import InvalidRatingException

class RatingSystem:
    def __init__(self):
        self._course_ratings: dict[str, list[float]] = {}
        self._instructor_ratings: dict[str, list[float]] = {}
    
    def rate_course(self, course: Course, rating: float) -> None:
        if not (1 <= rating <= 5):
            raise InvalidRatingException("Rating must be between 1 and 5")
        
        if course.course_id not in self._course_ratings:
            self._course_ratings[course.course_id] = []
        self._course_ratings[course.course_id].append(rating)
    
    def rate_instructor(self, instructor: Teacher, rating: float) -> None:
        if not (1 <= rating <= 5):
            raise InvalidRatingException("Rating must be between 1 and 5")
        
        if instructor.user_id not in self._instructor_ratings:
            self._instructor_ratings[instructor.user_id] = []
        self._instructor_ratings[instructor.user_id].append(rating)
    
    def get_course_rating(self, course: Course) -> float:
        ratings = self._course_ratings.get(course.course_id, [])
        return sum(ratings) / len(ratings) if ratings else 0.0
    
    def get_instructor_rating(self, instructor: Teacher) -> float:
        ratings = self._instructor_ratings.get(instructor.user_id, [])
        return sum(ratings) / len(ratings) if ratings else 0.0