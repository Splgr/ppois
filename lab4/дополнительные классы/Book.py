from functools import total_ordering

@total_ordering
class Book:
    """Класс книги с названием и годом издания"""
    def __init__(self, title: str, year: int):
        self.title = title
        self.year = year
    
    def __lt__(self, other):
        if isinstance(other, Book):
            return self.year < other.year
        return NotImplemented
    
    def __eq__(self, other):
        if isinstance(other, Book):
            return self.year == other.year
        return NotImplemented
    
    def __repr__(self):
        return f"Book('{self.title}', {self.year})"