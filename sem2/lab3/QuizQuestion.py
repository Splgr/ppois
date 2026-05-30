class QuizQuestion:
    def __init__(self, question_text: str, correct_answer: str):
        self._question_text = question_text
        self._correct_answer = correct_answer
        self._options: list[str] = []
        self._points: float = 1.0
    
    def add_option(self, option: str) -> None:
        self._options.append(option)
    
    def set_points(self, points: float) -> None:
        self._points = points
    
    def validate_answer(self, answer: str) -> bool:
        return answer == self._correct_answer