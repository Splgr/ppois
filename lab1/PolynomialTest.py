import unittest
import math
from Polynomial import Polynominal

class TestPolynominalInit(unittest.TestCase):
    
    # Тесты на корректное создание
    def test_valid_creation(self):
        """Тест корректного создания многочлена"""
        poly = Polynominal(2, [1, 2, 3])
        self.assertEqual(poly.degree, 2)
        self.assertEqual(poly.coefficients, [1, 2, 3])
    
    def test_valid_creation_with_float_coefficients(self):
        """Тест создания с дробными коэффициентами"""
        poly = Polynominal(2, [1.5, 2.0, 3.7])
        self.assertEqual(poly.degree, 2)
        self.assertEqual(poly.coefficients, [1.5, 2.0, 3.7])
    
    def test_valid_creation_with_tuple(self):
        """Тест создания с кортежем коэффициентов"""
        poly = Polynominal(2, (1, 2, 3))
        self.assertEqual(poly.degree, 2)
        self.assertEqual(poly.coefficients, [1, 2, 3])
    
    def test_zero_degree_polynomial(self):
        """Тест многочлена нулевой степени"""
        poly = Polynominal(0, [5])
        self.assertEqual(poly.degree, 0)
        self.assertEqual(poly.coefficients, [5])
    
    # Тесты на ошибки типа для degree
    def test_degree_not_int(self):
        """Тест на нецелую степень"""
        with self.assertRaises(TypeError) as context:
            Polynominal(2.5, [1, 2, 3])
        self.assertIn("Степень многочлена должна быть целым числом", str(context.exception))
    
    def test_degree_string(self):
        """Тест на строковую степень"""
        with self.assertRaises(TypeError) as context:
            Polynominal("2", [1, 2, 3])
        self.assertIn("Степень многочлена должна быть целым числом", str(context.exception))
    
    def test_degree_none(self):
        """Тест на None в степени"""
        with self.assertRaises(TypeError) as context:
            Polynominal(None, [1, 2, 3])
        self.assertIn("Степень многочлена должна быть целым числом", str(context.exception))
    
    # Тесты на отрицательную степень
    def test_negative_degree(self):
        """Тест на отрицательную степень"""
        with self.assertRaises(ValueError) as context:
            Polynominal(-1, [1])
        self.assertIn("Степень многочлена не может быть отрицательной", str(context.exception))
    
    def test_negative_degree_large(self):
        """Тест на большую отрицательную степень"""
        with self.assertRaises(ValueError) as context:
            Polynominal(-5, [1])
        self.assertIn("Степень многочлена не может быть отрицательной", str(context.exception))
    
    # Тесты на тип coefficients
    def test_coefficients_not_list(self):
        """Тест на неправильный тип коэффициентов"""
        with self.assertRaises(TypeError) as context:
            Polynominal(2, "1,2,3")
        self.assertIn("Коэффициенты должны быть списком или кортежем", str(context.exception))
    
    def test_coefficients_dict(self):
        """Тест на словарь вместо списка коэффициентов"""
        with self.assertRaises(TypeError) as context:
            Polynominal(2, {1: 1, 2: 2, 3: 3})
        self.assertIn("Коэффициенты должны быть списком или кортежем", str(context.exception))
    
    def test_coefficients_number(self):
        """Тест на число вместо списка коэффициентов"""
        with self.assertRaises(TypeError) as context:
            Polynominal(2, 123)
        self.assertIn("Коэффициенты должны быть списком или кортежем", str(context.exception))
    
    # Тесты на пустые коэффициенты
    def test_empty_coefficients(self):
        """Тест на пустой список коэффициентов"""
        with self.assertRaises(ValueError) as context:
            Polynominal(2, [])
        self.assertIn("Список коэффициентов не может быть пустым", str(context.exception))
    
    # Тесты на нечисловые коэффициенты
    def test_string_coefficient(self):
        """Тест на строковый коэффициент"""
        with self.assertRaises(TypeError) as context:
            Polynominal(2, [1, "a", 3])
        self.assertIn("должен быть числом", str(context.exception))
    
    def test_none_coefficient(self):
        """Тест на None в коэффициентах"""
        with self.assertRaises(TypeError) as context:
            Polynominal(2, [1, None, 3])
        self.assertIn("должен быть числом", str(context.exception))
    
    def test_list_coefficient(self):
        """Тест на список в коэффициентах"""
        with self.assertRaises(TypeError) as context:
            Polynominal(2, [1, [2], 3])
        self.assertIn("должен быть числом", str(context.exception))
    
    def test_multiple_invalid_coefficients(self):
        """Тест на несколько нечисловых коэффициентов"""
        with self.assertRaises(TypeError) as context:
            Polynominal(3, [1, "a", None, 4])
        # Проверяем что ошибка указывает на первый некорректный коэффициент
        self.assertIn("должен быть числом", str(context.exception))
    
    # Тесты на несоответствие длины
    def test_coefficients_length_too_short(self):
        """Тест когда коэффициентов меньше чем нужно"""
        with self.assertRaises(ValueError) as context:
            Polynominal(3, [1, 2, 3])  # Ожидается 4 коэффициента
        self.assertIn("ожидается 4 коэффициентов", str(context.exception).lower())
    
    def test_coefficients_length_too_long(self):
        """Тест когда коэффициентов больше чем нужно"""
        with self.assertRaises(ValueError) as context:
            Polynominal(2, [1, 2, 3, 4])  # Ожидается 3 коэффициента
        self.assertIn("ожидается 3 коэффициентов", str(context.exception).lower())
    
    def test_zero_degree_wrong_length(self):
        """Тест несоответствия длины для степени 0"""
        with self.assertRaises(ValueError) as context:
            Polynominal(0, [1, 2])  # Ожидается 1 коэффициент
        self.assertIn("ожидается 1 коэффициентов", str(context.exception).lower())
    
    # Тесты на нулевой старший коэффициент
    def test_zero_leading_coefficient(self):
        """Тест на нулевой старший коэффициент"""
        with self.assertRaises(ValueError) as context:
            Polynominal(2, [0, 1, 2])
        self.assertIn("Старший коэффициент не может быть нулевым для ненулевой степени", str(context.exception))
        
    def test_get_single_coefficient_by_index(self):
        """Тест получения одного коэффициента по индексу"""
        poly = Polynominal(3, [1, 2, 3, 4])
        self.assertEqual(poly[0], 1)  # Старший коэффициент
        self.assertEqual(poly[1], 2)
        self.assertEqual(poly[2], 3)
        self.assertEqual(poly[3], 4)  # Свободный член
    
    def test_get_single_coefficient_negative_index(self):
        """Тест получения коэффициента по отрицательному индексу"""
        poly = Polynominal(3, [1, 2, 3, 4])
        self.assertEqual(poly[-1], 4)  # Последний элемент
        self.assertEqual(poly[-2], 3)
        self.assertEqual(poly[-3], 2)
        self.assertEqual(poly[-4], 1)  # Первый элемент
    
    def test_get_slice_basic(self):
        """Тест базового среза"""
        poly = Polynominal(3, [1, 2, 3, 4])
        result = poly[1:3]  # Коэффициенты с индексами 1 и 2
        self.assertEqual(result, [2, 3])
        
    def test_evaluate_linear_polynomial(self):
        """Тест вычисления линейного многочлена"""
        poly = Polynominal(1, [2, 3])  # f(x) = 2x + 3
        self.assertEqual(poly._recieve_arg(0), 3)   # 2*0 + 3 = 3
        self.assertEqual(poly._recieve_arg(1), 5)   # 2*1 + 3 = 5
        self.assertEqual(poly._recieve_arg(2), 7)   # 2*2 + 3 = 7
        self.assertEqual(poly._recieve_arg(-1), 1)  # 2*(-1) + 3 = 1
    
    def test_evaluate_quadratic_polynomial(self):
        """Тест вычисления квадратного многочлена"""
        poly = Polynominal(2, [1, -2, 1])  # f(x) = x² - 2x + 1
        self.assertEqual(poly._recieve_arg(0), 1)   # 0 - 0 + 1 = 1
        self.assertEqual(poly._recieve_arg(1), 0)   # 1 - 2 + 1 = 0
        self.assertEqual(poly._recieve_arg(2), 1)   # 4 - 4 + 1 = 1
        self.assertEqual(poly._recieve_arg(-1), 4)  # 1 + 2 + 1 = 4
        
    def test_add_same_degree(self):
        """Тест сложения многочленов одинаковой степени"""
        p1 = Polynominal(2, [1, 2, 3]) 
        p2 = Polynominal(2, [4, 5, 6])  
        result = p1 + p2
        self.assertEqual(result.degree, 2)
        self.assertEqual(result.coefficients, [5, 7, 9]) 
    
    def test_add_different_degrees_first_higher(self):
        """Тест сложения, когда первый многочлен имеет большую степень"""
        p1 = Polynominal(3, [1, 2, 3, 4])
        p2 = Polynominal(2, [5, 6, 7])     
        result = p1 + p2
        self.assertEqual(result.degree, 3)
        self.assertEqual(result.coefficients, [1, 7, 9, 11])
    
    def test_add_different_degrees_second_higher(self):
        """Тест сложения, когда второй многочлен имеет большую степень"""
        p1 = Polynominal(2, [1, 2, 3])
        p2 = Polynominal(3, [4, 5, 6, 7])  
        result = p1 + p2
        self.assertEqual(result.degree, 3)
        self.assertEqual(result.coefficients, [4, 6, 8, 10])
        
    def test_iadd(self):
        """Тест +="""
        p1 = Polynominal(3, [1, 2, 3, 4])
        p2 = Polynominal(2, [5, 6, 7])
        p1 += p2
        self.assertEqual(p1.degree, 3)
        self.assertEqual(p1.coefficients, [1, 7, 9, 11])
        
    
    def test_sub_different_degrees_first_higher(self):
        """Тест вычитания, когда первый многочлен имеет большую степень"""
        p1 = Polynominal(3, [5, 6, 7, 8])  # 5 + 6x + 7x² + 8x³
        p2 = Polynominal(2, [1, 2, 3])     # 1 + 2x + 3x²
        result = p1 - p2
        self.assertEqual(result.degree, 3)
        self.assertEqual(result.coefficients, [5, 5, 5, 5])
    
    def test_sub_different_degrees_second_higher(self):
        """Тест вычитания, когда второй многочлен имеет большую степень"""
        p1 = Polynominal(2, [5, 6, 7])     # 5 + 6x + 7x²
        p2 = Polynominal(3, [1, 2, 3, 4])  # 1 + 2x + 3x² + 4x³
        result = p1 - p2
        self.assertEqual(result.degree, 3)
        self.assertEqual(result.coefficients, [-1, 3, 3, 3])
        
    def test_isub_different_degrees_first_higher(self):
        """Тест вычитания с присваиванием, когда первый многочлен имеет большую степень"""
        p1 = Polynominal(3, [5, 6, 7, 8])
        p2 = Polynominal(2, [1, 2, 3])
        p1-=p2
        self.assertEqual(p1.degree, 3)
        self.assertEqual(p1.coefficients, [5, 5, 5, 5])
    
    def test_isub_different_degrees_second_higher(self):
        """Тест вычитания с присваиванием, когда второй многочлен имеет большую степень"""
        p1 = Polynominal(2, [5, 6, 7])  
        p2 = Polynominal(3, [1, 2, 3, 4])  
        p1-=p2
        self.assertEqual(p1.degree, 3)
        self.assertEqual(p1.coefficients, [-1, 3, 3, 3])
        
    def test_mul_by_scalar_float(self):
        """Тест умножения на вещественное число"""
        p = Polynominal(2, [1, 2, 3])
        result = p * 1.5
        self.assertEqual(result.degree, 2)
        self.assertEqual(result.coefficients, [1.5, 3.0, 4.5])
        
    def test_mul_polynomials_different_degrees(self):
        """Тест умножения многочленов разной степени"""
        p1 = Polynominal(2, [1, 2, 3])
        p2 = Polynominal(1, [4, 5])
        result = p1 * p2
        self.assertEqual(result.degree, 3)
        self.assertEqual(result.coefficients, [4, 13, 22, 15]) 
    
    def test_imul_by_scalar_int(self):
        """Тест *= на целое число"""
        p = Polynominal(2, [1, 2, 3])
        p *= 2
        self.assertEqual(p.degree, 2)
        self.assertEqual(p.coefficients, [2, 4, 6])
    
    def test_imul_by_polynomial(self):
        """Тест *= на многочлен"""
        p1 = Polynominal(1, [1, 2])
        p2 = Polynominal(2, [3, 4, 5])
        p1 *= p2
        self.assertEqual(p1.degree, 3)
        self.assertEqual(p1.coefficients, [3, 10, 13, 10]) 
    
    def test_div_by_scalar_int(self):
        """Тест деления на целое число"""
        p = Polynominal(2, [4, 6, 8])  # 4 + 6x + 8x²
        result = p / 2
        self.assertEqual(result.degree, 2)
        self.assertEqual(result.coefficients, [2.0, 3.0, 4.0])
        
    def test_div_zero_division_error(self):
        """Тест деления на ноль"""
        p = Polynominal(2, [1, 2, 3])  # 1 + 2x + 3x²
        with self.assertRaises(ZeroDivisionError) as context:
            result = p / 0
        self.assertEqual(str(context.exception), "Деление на ноль")
        
    def test_itruediv_by_scalar_int(self):
        """Тест /= на целое число"""
        p = Polynominal(2, [4, 6, 8])
        original_id = id(p)
        p /= 2
        self.assertEqual(id(p), original_id)
        self.assertEqual(p.degree, 2)
        self.assertEqual(p.coefficients, [2.0, 3.0, 4.0]) 
    
    def test_itruediv_zero_division_error(self):
        """Тест /= на ноль"""
        p = Polynominal(2, [1, 2, 3])  # 1 + 2x + 3x²
        with self.assertRaises(ZeroDivisionError) as context:
            p /= 0
        self.assertEqual(str(context.exception), "Деление на ноль")
        
    def test_itruediv_by_polynomial_type_error(self):
        """Тест /= на многочлен"""
        p1 = Polynominal(2, [1, 2, 3])
        p2 = Polynominal(1, [1, 1])
        with self.assertRaises(TypeError) as context:
            p1 /= p2
        self.assertEqual(str(context.exception), "Деление возможно только на число")

if __name__ == '__main__':
    unittest.main()