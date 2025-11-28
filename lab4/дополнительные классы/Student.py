from functools import total_ordering

@total_ordering
class Student:
    """Класс студента с именем и средним баллом"""
    def __init__(self, name: str, gpa: float):
        self.name = name
        self.gpa = gpa
    
    def __lt__(self, other):
        if isinstance(other, Student):
            return self.gpa < other.gpa
        return NotImplemented
    
    def __eq__(self, other):
        if isinstance(other, Student):
            return self.gpa == other.gpa
        return NotImplemented
    
    def __repr__(self):
        return f"Student('{self.name}', GPA: {self.gpa})"