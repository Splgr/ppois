from Lesson import Lesson

class Module:
    def __init__(self, module_id: str, title: str):
        self._module_id = module_id
        self._title = title
        self._lessons: list[Lesson] = []
        self._description: str = ""
    
    def add_lesson(self, lesson: Lesson) -> None:
        self._lessons.append(lesson)
    
    def set_description(self, description: str) -> None:
        self._description = description
    
    def get_total_duration(self) -> int:
        return sum(lesson.calculate_total_duration() for lesson in self._lessons)
    
    def get_lesson_count(self) -> int:
        return len(self._lessons)