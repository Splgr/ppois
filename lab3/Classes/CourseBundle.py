from Course import Course
from Student import Student
from exceptions import PaymentRequiredException

class CourseBundle:
    def __init__(self, bundle_id: str, name: str):
        self._bundle_id = bundle_id
        self._name = name
        self._courses: list[Course] = []
        self._price: float = 0.0
    
    def add_course(self, course: Course) -> None:
        if course not in self._courses:
            self._courses.append(course)
    
    def set_price(self, price: float) -> None:
        self._price = price
    
    def calculate_savings(self) -> float:
        individual_price = sum(100 for _ in self._courses)
        return individual_price - self._price
    
    def get_course_count(self) -> int:
        return len(self._courses)
    
    def purchase_bundle(self, student: Student) -> None:
        if self._price > 0:
            raise PaymentRequiredException("Payment required to purchase this bundle")
        
        for course in self._courses:
            student.enroll_in_course(course)