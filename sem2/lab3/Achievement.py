class Achievement:
    def __init__(self, name: str):
        self._name = name
        self._description: str = ""
        self._points: int = 0
    
    def set_description(self, description: str) -> None:
        self._description = description
    
    def set_points(self, points: int) -> None:
        self._points = points
    
    def get_achievement_info(self) -> dict:
        return {
            "name": self._name,
            "description": self._description,
            "points": self._points
        }