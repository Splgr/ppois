from functools import total_ordering

@total_ordering
class Product:
    """Класс продукта с названием и ценой"""
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price
    
    def __lt__(self, other):
        if isinstance(other, Product):
            return self.price < other.price
        return NotImplemented
    
    def __eq__(self, other):
        if isinstance(other, Product):
            return self.price == other.price
        return NotImplemented
    
    def __repr__(self):
        return f"Product('{self.name}', ${self.price})"