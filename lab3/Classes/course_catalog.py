from course import Course

class CourseCatalog:
    def __init__(self):
        self._courses: list[Course] = []
        self._categories: dict[str, list[Course]] = {}
    
    def add_course(self, course: Course) -> None:
        self._courses.append(course)
    
    def search_courses(self, query: str) -> list[Course]:
        results = []
        for course in self._courses:
            if query.lower() in course._title.lower():
                results.append(course)
        return results
    
    def add_course_to_category(self, course: Course, category: str) -> None:
        if category not in self._categories:
            self._categories[category] = []
        if course not in self._categories[category]:
            self._categories[category].append(course)
    
    def get_courses_by_category(self, category: str) -> list[Course]:
        return self._categories.get(category, [])