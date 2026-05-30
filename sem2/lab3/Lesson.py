from LearningContent import LearningContent
from exceptions import ContentNotApprovedException

class Lesson:
    def __init__(self, lesson_id: str, title: str):
        self._lesson_id = lesson_id
        self._title = title
        self._materials: list[LearningContent] = []
        self._duration_minutes: int = 0
        self._learning_objectives: list[str] = []
    
    def add_material(self, material: LearningContent) -> None:
        if not material._is_approved:
            raise ContentNotApprovedException("Cannot add unapproved content to lesson")
        self._materials.append(material)
    
    def set_duration(self, minutes: int) -> None:
        self._duration_minutes = minutes
    
    def add_learning_objective(self, objective: str) -> None:
        self._learning_objectives.append(objective)
    
    def calculate_total_duration(self) -> int:
        material_duration = len(self._materials) * 30
        return self._duration_minutes + material_duration