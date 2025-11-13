from course import Course
from exceptions import CourseNotFoundException

class CourseManager:
    def __init__(self):
        self._courses: list[Course] = []
        self._course_categories: dict[str, list[Course]] = {}
    
    def create_course(self, teacher, course_data: dict) -> Course:
        course = Course(course_data['course_id'], course_data['title'], teacher)
        self._courses.append(course)
        return course
    
    def get_course_by_id(self, course_id: str) -> Course:
        for course in self._courses:
            if course.course_id == course_id:
                return course
        raise CourseNotFoundException(f"Course with ID {course_id} not found")
    
    def get_courses_by_instructor(self, instructor) -> list[Course]:
        return [course for course in self._courses if course._instructor == instructor]
    
    def add_course_to_category(self, course: Course, category: str) -> None:
        if category not in self._course_categories:
            self._course_categories[category] = []
        if course not in self._course_categories[category]:
            self._course_categories[category].append(course)
    
    def search_courses(self, query: str) -> list[Course]:
        results = []
        for course in self._courses:
            if (query.lower() in course._title.lower() or 
                any(query.lower() in tag.lower() for tag in course._tags)):
                results.append(course)
        return results