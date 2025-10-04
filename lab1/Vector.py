import math
class Vector:
    def __init__(self, x1, y1, z1, x2, y2, z2):
        # Проверка типов входных данных
        if not all(isinstance(coord, (int, float)) for coord in [x1, y1, z1, x2, y2, z2]):
            raise TypeError("Все координаты должны быть числами!")
        
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
    
    @property
    def dx(self):
        return self.x2 - self.x1
    
    @property
    def dy(self):
        return self.y2 - self.y1
    
    @property
    def dz(self):
        return self.z2 - self.z1
    
    @property
    def length(self):
        return math.sqrt(self.dx**2 + self.dy**2 + self.dz**2)
    
    @property
    def coordinates(self):
        return (self.dx, self.dy, self.dz)
    
    def _validate_vector(self, other):
        """Проверка что other является вектором"""
        if not isinstance(other, Vector):
            raise TypeError("Операция возможна только между векторами")
        return True
    
    def _validate_number(self, other):
        """Проверка что other является числом"""
        if not isinstance(other, (int, float)):
            raise TypeError("Операция возможна только с числами")
        return True
    
    # Сложение +
    def __add__(self, other):
        self._validate_vector(other)
        return Vector(self.x1, self.y1, self.z1,
                    self.x2 + other.dx,
                    self.y2 + other.dy,
                    self.z2 + other.dz)
    
    # Сложение +=
    def __iadd__(self, other):
        self._validate_vector(other)
        self.x2 += other.dx
        self.y2 += other.dy
        self.z2 += other.dz
        return self
        
    # Вычитание -
    def __sub__(self, other):
        self._validate_vector(other)
        return Vector(self.x1, self.y1, self.z1,
                        self.x2 - other.dx,
                        self.y2 - other.dy,
                        self.z2 - other.dz)
        
    # Вычитание -=
    def __isub__(self, other):
        self._validate_vector(other)
        self.x2 -= other.dx
        self.y2 -= other.dy
        self.z2 -= other.dz
        return self
    
    def _dot(self, other):
        """Скалярное произведение векторов"""
        self._validate_vector(other)
        return self.dx * other.dx + self.dy * other.dy + self.dz * other.dz
    
    # Умножение: вектор * число ИЛИ вектор * вектор (векторное произведение)
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            # Умножение вектора на число
            return Vector(self.x1, self.y1, self.z1,
                         self.x1 + self.dx * other,
                         self.y1 + self.dy * other,
                         self.z1 + self.dz * other)
        
        elif isinstance(other, Vector):
            # Векторное произведение векторов
            return Vector(0, 0, 0,
                         self.dy * other.dz - self.dz * other.dy,
                         self.dz * other.dx - self.dx * other.dz,
                         self.dx * other.dy - self.dy * other.dx), self._dot(other)
        else:
            raise TypeError("Умножение возможно только на число или другой вектор")
    
    # Умножение с присваиванием: *= для чисел и векторов (векторное произведение)
    def __imul__(self, other):
        if isinstance(other, (int, float)):
            # Умножение вектора на число с присваиванием
            self.x2 = self.x1 + self.dx * other
            self.y2 = self.y1 + self.dy * other
            self.z2 = self.z1 + self.dz * other
            return self
        elif isinstance(other, Vector):
            # Векторное произведение с присваиванием
            result_vector, _ = self * other
            self.x1, self.y1, self.z1 = result_vector.x1, result_vector.y1, result_vector.z1
            self.x2, self.y2, self.z2 = result_vector.x2, result_vector.y2, result_vector.z2
            return self
        else:
            raise TypeError("Умножение возможно только на число или другой вектор")
        
    # Деление на число /
    def __truediv__(self, scalar):
        self._validate_number(scalar)
        if scalar == 0:
            raise ZeroDivisionError("Невозможно разделить вектор на ноль")
        return Vector(self.x1, self.y1, self.z1,
                        self.x1 + self.dx / scalar,
                        self.y1 + self.dy / scalar,
                        self.z1 + self.dz / scalar)
        
    # Деление на число /=
    def __itruediv__(self, scalar):
        self._validate_number(scalar)
        if scalar == 0:
            raise ZeroDivisionError("Невозможно разделить вектор на ноль")
        self.x2 = self.x1 + self.dx / scalar
        self.y2 = self.y1 + self.dy / scalar
        self.z2 = self.z1 + self.dz / scalar
        return self
        
    # Косинус между векторами ^
    def __xor__(self, other):
        self._validate_vector(other)
        mul_scalar = self._dot(other)
        mul_length = self.length * other.length
        if mul_length == 0:
            raise ValueError("Один из векторов имеет нулевую длину")
        return mul_scalar / mul_length
    
    
    # Сравнение векторов ==
    def __eq__(self, other):
        self._validate_vector(other)
        return (math.isclose(self.x1, other.x1) and 
            math.isclose(self.y1, other.y1) and 
            math.isclose(self.z1, other.z1) and
            math.isclose(self.x2, other.x2) and 
            math.isclose(self.y2, other.y2) and 
            math.isclose(self.z2, other.z2))
        
    # Сравнение длин векторов <
    def __lt__(self, other):
        self._validate_vector(other)
        return self.length < other.length
     
    # Сравнение длин векторов <=
    def __le__(self, other):
        self._validate_vector(other)
        return self.length <= other.length
        
    # Сравнение длин векторов >
    def __gt__(self, other):
        self._validate_vector(other)
        return self.length > other.length
        
    # Сравнение длин векторов >=
    def __ge__(self, other):
        self._validate_vector(other)
        return self.length >= other.length