import unittest
import math
from Vector import Vector
class Test_Vector(unittest.TestCase):
    def test_valid_vector_creation(self):
        """Тест создания вектора с корректными числами"""
        vec = Vector(1, 2, 3, 4, 5, 6)
        self.assertIsInstance(vec, Vector) # является ли vec вектором, или он не создался из-за какойто-то ошибки, символ не тот
        self.assertEqual(vec.x1, 1.0)  # точно ли 1 и 1.0 то же самое

    def test_vector_with_string_coordinate_raises_error(self):
        """Тест ошибки при создании вектора со строкой"""
        with self.assertRaises(TypeError) as context:
            Vector("1", 2, 3, 4, 5, 6)  # Первая координата - строка
        self.assertIn("Все координаты должны быть числами", str(context.exception))#мало того, что ошибка есть, текст ошибки тоже должен совпадать
    
    def test_addition(self):
        """Тест сложения двух векторов"""
        vec1 = Vector(1, 2, 3, 4, 5, 6)
        vec2 = Vector(3, 5, 6, 2, 1, 5)
        self.assertEqual(vec1 + vec2, Vector(1, 2, 3, 3, 1, 5))
    
    def test_iadd_valid(self):
        """Тест корректного сложения += """
        v1 = Vector(1, 2, 3, 4, 5, 6)
        v2 = Vector(4, 5, 6, 7, 3, 5)
        v1 += v2
        self.assertEqual(v1.x1, 1)
        self.assertEqual(v1.y1, 2)
        self.assertEqual(v1.z1, 3)
        self.assertEqual(v1.x2, 7)
        self.assertEqual(v1.y2, 3)
        self.assertEqual(v1.z2, 5)
        
    def test_add_valid(self):
        """Тест корректного сложения + """
        v1 = Vector(1, 2, 3, 4, 5, 6)
        v2 = Vector(4, 5, 6, 7, 3, 5)
        result = v1 + v2     
        
        self.assertEqual(result.x1, 1)
        self.assertEqual(result.y1, 2)
        self.assertEqual(result.z1, 3)
        self.assertEqual(result.x2, 7)  # 4 + 3 = 7
        self.assertEqual(result.y2, 3)  # 5 - 2 = 3
        self.assertEqual(result.z2, 5)

    def test_sub_valid(self):
        """Тест корректного вычитания - """
        v1 = Vector(1, 2, 3, 4, 5, 6)
        v2 = Vector(4, 5, 6, 7, 3, 5)
        result = v1 - v2
        
        self.assertEqual(result.x1, 1)  # начальная точка сохраняется
        self.assertEqual(result.y1, 2)
        self.assertEqual(result.z1, 3)
        self.assertEqual(result.x2, 1)  # 4 - 3 = 1
        self.assertEqual(result.y2, 7)  # 5 - (-2) = 7
        self.assertEqual(result.z2, 7)  # 6 - (-1) = 7

    def test_isub_valid(self):
        """Тест корректного вычитания -= """
        v1 = Vector(1, 2, 3, 4, 5, 6)  # вектор (3, 3, 3)
        v2 = Vector(4, 5, 6, 7, 3, 5)  # вектор (3, -2, -1)
        v1 -= v2
        
        self.assertEqual(v1.x1, 1)  # начальная точка не изменилась
        self.assertEqual(v1.y1, 2)
        self.assertEqual(v1.z1, 3)
        self.assertEqual(v1.x2, 1)  # 4 - 3 = 1
        self.assertEqual(v1.y2, 7)  # 5 - (-2) = 7
        self.assertEqual(v1.z2, 7)  # 6 - (-1) = 7

    def test_iadd_invalid_type(self):
        """Тест попытки сложить вектор с не-вектором"""
        v1 = Vector(1, 4, 5, 6, 2, 4)
        with self.assertRaises(TypeError):
            v1 += 5  # Попытка сложить с числом
        
        with self.assertRaises(TypeError):
            v1 += "string"  # Попытка сложить со строкой
    
    def test_vector_initialization_with_6_args(self):
        """Тест на проверку корректного количества аргументов"""
        v = Vector(1, 2, 3, 4, 5, 6)
        self.assertIsInstance(v, Vector)
        
    def test_vector_initialization_with_5_args(self):
        v = Vector(1, 2, 3, 4, 5, 6)
        with self.assertRaises(TypeError):
            Vector(1, 2, 3, 4, 5)  # Не хватает одного аргумента
            
    def test_vector_initialization_with_7_args(self):
        with self.assertRaises(TypeError):
            Vector(1, 2, 3, 4, 5, 6, 7) 

    def test_multiplication_scalar(self):
        """Тест на проверку корректного умножения вектора на скаляр/число"""
        v1 = Vector(0, 0, 0, 2, 3, 4)
        result = v1 * 3
        # Проверяем, что координаты правильно умножились
        self.assertEqual(result.x1, 0)
        self.assertEqual(result.y1, 0)
        self.assertEqual(result.z1, 0)
        self.assertEqual(result.dx, 6)   # 2 * 3 = 6
        self.assertEqual(result.dy, 9)   # 3 * 3 = 9
        self.assertEqual(result.dz, 12)  # 4 * 3 = 12
        
    def test_multiplication_vector1(self):
        """Тест на проверку корректного умножения вектора на вектор векторно"""
        v1 = Vector(0, 0, 0, 2, 3, 4)
        v2 = Vector(0, 0, 0, 1, 0, -1)
        cross_result, _ = v1 * v2
        
        self.assertEqual(cross_result.x1, 0)
        self.assertEqual(cross_result.y1, 0) 
        self.assertEqual(cross_result.z1, 0)
        self.assertEqual(cross_result.dx, -3)   # конец вектора x: 3*(-1) - 4*0 = -3
        self.assertEqual(cross_result.dy, 6)    # конец вектора y: 4*1 - 2*(-1) = 6
        self.assertEqual(cross_result.dz, -3)   # конец вектора z: 2*0 - 3*1 = -3
        
    def test_multiplication_vector2(self):
        """Тест на проверку корректного умножения вектора на вектор скалярно"""
        v1 = Vector(0, 0, 0, 2, 3, 4)
        v2 = Vector(0, 0, 0, 1, 0, -1)
        _, dot_result = v1 * v2
        self.assertEqual(dot_result, -2)
        
    def test_multiplication_with_error(self):
        v = Vector(0, 0, 0, 2, 3, 4)
        '''Тест ошибки при неправильном типе'''
        with self.assertRaises(TypeError):
            v * "не число"
        
    def test_imul(self):
        """Тест на проверку корректного умножения c присваиванием"""
        v = Vector(1, 2, 3, 4, 5, 6) 
        result = v * 2
        v *= 2
        # Проверяем, что координаты изменились правильно
        self.assertEqual(v.x1, 1)  # Начальная точка не должна меняться
        self.assertEqual(v.y1, 2)
        self.assertEqual(v.z1, 3)
        self.assertEqual(v.x2, 7)  # 1 + 3*2 = 7
        self.assertEqual(v.y2, 8)  # 2 + 3*2 = 8  
        self.assertEqual(v.z2, 9)  # 3 + 3*2 = 9
        
        # Сравниваем с результатом обычного умножения
        self.assertEqual(v.x1, result.x1)
        self.assertEqual(v.y1, result.y1)
        self.assertEqual(v.z1, result.z1)
        self.assertEqual(v.x2, result.x2)
        self.assertEqual(v.y2, result.y2)
        self.assertEqual(v.z2, result.z2)
        
    def test_imul_vector(self):
        '''Тест векторного умножения с присваиванием'''
        v1 = Vector(0, 0, 0, 2, 3, 4)
        v2 = Vector(0, 0, 0, 1, 0, -1)
        
        cross_result, _ = v1 * v2  # Обычное умножение для сравнения
        v1 *= v2  # Умножение с присваиванием
        
        self.assertEqual(v1.x1, cross_result.x1)
        self.assertEqual(v1.y1, cross_result.y1)
        self.assertEqual(v1.z1, cross_result.z1)
        self.assertEqual(v1.x2, cross_result.x2)
        self.assertEqual(v1.y2, cross_result.y2)
        self.assertEqual(v1.z2, cross_result.z2)
        
    def test_imul_with_error(self):
        '''Проверка ошибок при умножении с присваиванием'''
        v = Vector(0, 0, 0, 2, 3, 4)
        with self.assertRaises(TypeError):
            v *= "error"
        with self.assertRaises(TypeError):
            v *= [1, 2, 3]
            
    def test_truediv(self):
        """Тест на проверку корректного деления вектора на число"""
        v = Vector(1, 2, 3, 5, 8, 11)

        result = v / 2
        self.assertEqual((result.x1, result.y1, result.z1, result.x2, result.y2, result.z2), 
                        (1, 2, 3, 3, 5, 7))

        with self.assertRaises(ZeroDivisionError):
            v / 0.0
            
    def test_truediv_with_error(self):
        """Тест на проверку вывода ошибки при делении не на число"""
        v = Vector(1, 2, 3, 5, 8, 11)

        with self.assertRaises(TypeError):
            v / "2"
        with self.assertRaises(TypeError):
            v / [1, 2, 3]
        with self.assertRaises(TypeError):
            v / None
            
    def test_itruediv(self):
        """Тест на проверку корректного деления вектора на число с присваиванием"""
        v = Vector(1, 2, 3, 5, 8, 11)
        
        # Деление с присваиванием
        result = v / 2
        v /= 2

        # Проверяем правильность вычислений
        self.assertEqual(v.x1, 1)  # Начальная точка не меняется
        self.assertEqual(v.y1, 2)
        self.assertEqual(v.z1, 3)
        self.assertEqual(v.x2, 3)  # 1 + 4/2 = 3
        self.assertEqual(v.y2, 5)  # 2 + 6/2 = 5
        self.assertEqual(v.z2, 7)  # 3 + 8/2 = 7
        
        # Сравниваем с результатом обычного деления
        self.assertEqual((v.x1, v.y1, v.z1, v.x2, v.y2, v.z2), 
                        (result.x1, result.y1, result.z1, result.x2, result.y2, result.z2))
        
        # Тест деления на отрицательное число
        v_neg = Vector(0, 0, 0, 4, 6, 8)
        v_neg /= -2
        self.assertEqual((v_neg.x2, v_neg.y2, v_neg.z2), (-2, -3, -4))
        
    def test_itruediv_with_0(self):
        '''Тест на проверку выводаошибки при делении на 0'''
        v = Vector(1, 2, 3, 5, 8, 11)
        with self.assertRaises(ZeroDivisionError):
            v /= 0
            
    def test_itruediv_with_error(self):
        v = Vector(1, 2, 3, 5, 8, 11)
        with self.assertRaises(TypeError):
            v /= "2"
        with self.assertRaises(TypeError):
            v /= [1, 2, 3]
        with self.assertRaises(TypeError):
            v /= None

    def test_vector_xor_method(self):
        """Тест на проверку корректного нахождения косинуса между векторами"""
        v1 = Vector(0, 0, 0, 1, 0, 0)
        v2 = Vector(0, 0, 0, 2, 0, 0)
        self.assertEqual(v1 ^ v2, 1.0)
        
        v3 = Vector(0, 0, 0, -3, 0, 0)
        self.assertEqual(v1 ^ v3, -1.0)

        v4 = Vector(0, 0, 0, 0, 1, 0)
        self.assertEqual(v1 ^ v4, 0.0)
         
        
    def test_less(self):
        short_vec = Vector(0, 0, 0, 1, 0, 0) # 1
        medium_vec = Vector(0, 0, 0, 3, 4, 0) # 5
        long_vec = Vector(0, 0, 0, 6, 8, 0) # 10
        same_as_medium = Vector(0, 0, 0, 3, 4, 0)
        
        self.assertTrue(short_vec < medium_vec)
        self.assertTrue(medium_vec < long_vec)
        self.assertFalse(medium_vec < short_vec)
        self.assertFalse(medium_vec < same_as_medium)
        
    def test_less_or_equal(self):
        short_vec = Vector(0, 0, 0, 1, 0, 0) # 1
        medium_vec = Vector(0, 0, 0, 3, 4, 0) # 5
        long_vec = Vector(0, 0, 0, 6, 8, 0) # 10
        same_as_medium = Vector(0, 0, 0, 3, 4, 0)
        self.assertTrue(short_vec <= medium_vec)
        self.assertTrue(medium_vec <= long_vec)
        self.assertTrue(medium_vec <= same_as_medium)
        self.assertFalse(long_vec <= medium_vec)
        
    def test_more(self):
        short_vec = Vector(0, 0, 0, 1, 0, 0) # 1
        medium_vec = Vector(0, 0, 0, 3, 4, 0) # 5
        long_vec = Vector(0, 0, 0, 6, 8, 0) # 10
        same_as_medium = Vector(0, 0, 0, 3, 4, 0)
        
        self.assertTrue(long_vec > medium_vec)
        self.assertTrue(medium_vec > short_vec)
        self.assertFalse(short_vec > medium_vec)
        self.assertFalse(medium_vec > same_as_medium)
        
    def test_more_or_equal(self):
        short_vec = Vector(0, 0, 0, 1, 0, 0) # 1
        medium_vec = Vector(0, 0, 0, 3, 4, 0) # 5
        long_vec = Vector(0, 0, 0, 6, 8, 0) # 10
        same_as_medium = Vector(0, 0, 0, 3, 4, 0)
        self.assertTrue(long_vec >= medium_vec)
        self.assertTrue(medium_vec >= short_vec)
        self.assertTrue(medium_vec >= same_as_medium)
        self.assertFalse(short_vec >= medium_vec)
        
    def test_vector_coordinates_property(self):
        """Тест на определение координат вектора"""
        v1 = Vector(0, 0, 0, 1, 2, 3)  # (1,2,3)
        self.assertEqual(v1.coordinates, (1, 2, 3))
        
        v2 = Vector(0, 0, 0, -1, -2, -3)  # (-1,-2,-3)
        self.assertEqual(v2.coordinates, (-1, -2, -3))

        v3 = Vector(1, 2, 3, 4, 6, 9)
        self.assertEqual(v3.coordinates, (3, 4, 6))
        
        v4 = Vector(0, 0, 0, 1.5, 2.5, 3.5)
        self.assertEqual(v4.coordinates, (1.5, 2.5, 3.5))
        
    def test_vector_length_property(self):
        """Тест свойства length (длина вектора)"""
        v1 = Vector(0, 0, 0, 3, 0, 0)
        self.assertEqual(v1.length, 3.0)
        
        v2 = Vector(0, 0, 0, 0, 4, 0)
        self.assertEqual(v2.length, 4.0)
    
        v3 = Vector(0, 0, 0, 0, 0, 5)
        self.assertEqual(v3.length, 5.0)

        v4 = Vector(0, 0, 0, 3, 4, 0) 
        self.assertEqual(v4.length, 5.0) 
        
        v5 = Vector(0, 0, 0, 2, 3, 6)
        expected = math.sqrt(2**2 + 3**2 + 6**2)
        self.assertEqual(v5.length, expected)

        v6 = Vector(0, 0, 0, -3, -4, 0)
        self.assertEqual(v6.length, 5.0)