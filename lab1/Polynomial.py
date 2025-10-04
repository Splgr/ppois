import math
from PolynomialView import PolynomialView
class Polynominal:
    def __init__(self, degree, coefficients):
        # Проверка типа degree
        if not isinstance(degree, int):
            raise TypeError("Степень многочлена должна быть целым числом")
        
        # Проверка что degree не отрицательный
        if degree < 0:
            raise ValueError("Степень многочлена не может быть отрицательной")
        
        # Проверка типа coefficients
        if not isinstance(coefficients, (list, tuple)):
            raise TypeError("Коэффициенты должны быть списком или кортежем")
        
        # Проверка что coefficients не пустой
        if len(coefficients) == 0:
            raise ValueError("Список коэффициентов не может быть пустым")
        
        # Проверка что все элементы coefficients - числа
        for i, coef in enumerate(coefficients):
            if not isinstance(coef, (int, float)):
                raise TypeError(f"Коэффициент с индексом {i} должен быть числом, получен {type(coef)}")
        
        def __str__(self):
            return self.view.to_str(self)
        
        # Проверка соответствия степени и количества коэффициентов
        if len(coefficients) != degree + 1:
            raise ValueError(f"Для степени {degree} ожидается {degree + 1} коэффициентов, получено {len(coefficients)}")
        
        # Проверка что старший коэффициент не нулевой (если степень > 0)
        if degree > 0 and coefficients[0] == 0:
            raise ValueError("Старший коэффициент не может быть нулевым для ненулевой степени")
        
        
        self.degree = degree
        self.coefficients = list(coefficients)  # Преобразуем в список на случай если был кортеж
    
    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.coefficients[key]
        elif isinstance(key, int):
            return self.coefficients[key]
        else:
            raise TypeError("Ключ должен быть int или slice")
    
    def _recieve_arg(self, x):
        result = 0
        for i in range(self.degree, -1, -1):
            result += x**i*int(self.coefficients[::-1][i])
        return result
    
        
    def __add__(self, other):
        max_degree = max(self.degree, other.degree)
        new_coef = [0] * (max_degree + 1)

        offset1 = max_degree - self.degree
        for i in range(self.degree + 1):
            new_coef[offset1 + i] += self.coefficients[i]
        
        # Добавляем коэффициенты второго многочлена
        offset2 = max_degree - other.degree
        for i in range(other.degree + 1):
            new_coef[offset2 + i] += other.coefficients[i]
        
        return Polynominal(max_degree, new_coef)
    
    def __iadd__(self, other):
        max_degree = max(self.degree, other.degree)
        new_coef = [0] * (max_degree + 1)

        offset1 = max_degree - self.degree
        for i in range(self.degree + 1):
            new_coef[offset1 + i] += self.coefficients[i]

        offset2 = max_degree - other.degree
        for i in range(other.degree + 1):
            new_coef[offset2 + i] += other.coefficients[i]

        self.degree = max_degree
        self.coefficients = new_coef
        
        return self
    
        # Вычитание -
    def __sub__(self, other):
        max_degree = max(self.degree, other.degree)
        new_coef = [0] * (max_degree + 1)
        
        # Добавляем коэффициенты первого многочлена
        offset1 = max_degree - self.degree
        for i in range(self.degree + 1):
            new_coef[offset1 + i] += self.coefficients[i]
        
        # Вычитаем коэффициенты второго многочлена
        offset2 = max_degree - other.degree
        for i in range(other.degree + 1):
            new_coef[offset2 + i] -= other.coefficients[i]
        
        return Polynominal(max_degree, new_coef)
    
    # Вычитание с присваиванием -=
    def __isub__(self, other):
        max_degree = max(self.degree, other.degree)
        new_coef = [0] * (max_degree + 1)
        
        offset1 = max_degree - self.degree
        for i in range(self.degree + 1):
            new_coef[offset1 + i] += self.coefficients[i]
        
        offset2 = max_degree - other.degree
        for i in range(other.degree + 1):
            new_coef[offset2 + i] -= other.coefficients[i]
        self.degree = max_degree
        self.coefficients = new_coef
        return self
    
    def __mul__(self, other):
        # Умножение на число
        if isinstance(other, (int, float)):
            new_coef = [coef * other for coef in self.coefficients]
            return Polynominal(self.degree, new_coef)
        # Умножение на многочлен
        new_degree = self.degree + other.degree
        new_coef = [0] * (new_degree + 1)
        
        for i in range(self.degree + 1):
            for j in range(other.degree + 1):
                new_coef[i + j] += self.coefficients[i] * other.coefficients[j]
        
        return Polynominal(new_degree, new_coef)
    # Умножение с присваиванием *=
    def __imul__(self, other):
        if isinstance(other, (int, float)):
            new_coef = [coef * other for coef in self.coefficients]
            self.coefficients = new_coef
            # Степень не меняется при умножении на число
            return self
        else:
            new_degree = self.degree + other.degree
            new_coef = [0] * (new_degree + 1)
            
            for i in range(self.degree + 1):
                for j in range(other.degree + 1):
                    new_coef[i + j] += self.coefficients[i] * other.coefficients[j]
            
            self.degree = new_degree
            self.coefficients = new_coef
            return self
    # Деление на число /
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Деление на ноль")
            new_coef = [round(coef / other, 3) for coef in self.coefficients]
            return Polynominal(self.degree, new_coef)
        else:
            raise TypeError("Деление возможно только на число")
    # Деление на число с присваиванием /=
    def __itruediv__(self, other):
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Деление на ноль")
            self.coefficients = [round(coef / other, 3) for coef in self.coefficients]
            return self
        else:
            raise TypeError("Деление возможно только на число")
