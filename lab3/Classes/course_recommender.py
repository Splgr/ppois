from course_catalog import CourseCatalog
from course import Course
from enums import CourseStatus
from exceptions import CourseNotPublishedException

class CourseRecommender:
    def __init__(self, course_catalog: CourseCatalog):
        self._course_catalog = course_catalog
    
    def recommend_courses(self) -> list[Course]:
        published_courses = [course for course in self._course_catalog._courses 
                           if course._status == CourseStatus.PUBLISHED]
        return published_courses[:3]
    
    def calculate_recommendation_confidence(self, course: Course) -> float:
        if course._status != CourseStatus.PUBLISHED:
            raise CourseNotPublishedException("Cannot recommend unpublished course")
        return 0.7