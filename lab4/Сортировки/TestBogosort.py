import unittest
import random
from Product import Product
from Student import Student
from Book import Book
from Bogosort import BogoSort

class TestBogosort(unittest.TestCase):
    
    def setUp(self):
        """Устанавливаем seed для предсказуемости тестов"""
        random.seed(42)
    
    def test_empty_list(self):
        """Тест пустого списка"""
        sorter = BogoSort([])
        result = sorter.sort()
        self.assertEqual(result, [])
        self.assertTrue(sorter.is_sorted())
    
    def test_single_element(self):
        """Тест списка с одним элементом"""
        sorter = BogoSort([42])
        result = sorter.sort()
        self.assertEqual(result, [42])
        self.assertTrue(sorter.is_sorted())
    
    def test_already_sorted(self):
        """Тест уже отсортированного массива"""
        sorter = BogoSort([1, 2, 3, 4, 5])
        result = sorter.sort()
        self.assertEqual(result, [1, 2, 3, 4, 5])
        self.assertTrue(sorter.is_sorted())
    
    def test_reverse_sorted(self):
        """Тест обратно отсортированного массива"""
        sorter = BogoSort([5, 4, 3, 2, 1])
        result = sorter.sort()
        self.assertEqual(result, [1, 2, 3, 4, 5])
        self.assertTrue(sorter.is_sorted())
    
    def test_duplicate_elements(self):
        """Тест с дублирующимися элементами"""
        sorter = BogoSort([3, 1, 3, 2, 1])
        result = sorter.sort()
        self.assertEqual(result, [1, 1, 2, 3, 3])
        self.assertTrue(sorter.is_sorted())
    
    def test_negative_numbers(self):
        """Тест с отрицательными числами"""
        sorter = BogoSort([-3, -1, -2, 0, -5])
        result = sorter.sort()
        self.assertEqual(result, [-5, -3, -2, -1, 0])
        self.assertTrue(sorter.is_sorted())
    
    def test_strings_sorting(self):
        """Тест сортировки строк"""
        sorter = BogoSort(["banana", "apple", "cherry", "date"])
        result = sorter.sort()
        self.assertEqual(result, ["apple", "banana", "cherry", "date"])
        self.assertTrue(sorter.is_sorted())
    
    def test_product_class_sorting(self):
        """Тест сортировки объектов Product по цене"""
        products = [
            Product("Laptop", 999.99),
            Product("Mouse", 25.50),
            Product("Keyboard", 75.00),
            Product("Monitor", 299.99),
            Product("Headphones", 150.00)
        ]
        sorter = BogoSort(products)
        result = sorter.sort()
        
        # Проверяем что отсортировано по цене
        expected_prices = [25.50, 75.00, 150.00, 299.99, 999.99]
        actual_prices = [p.price for p in result]
        self.assertEqual(actual_prices, expected_prices)
        self.assertTrue(sorter.is_sorted())
        
        # Проверяем что названия соответствуют ценам
        expected_names = ["Mouse", "Keyboard", "Headphones", "Monitor", "Laptop"]
        actual_names = [p.name for p in result]
        self.assertEqual(actual_names, expected_names)
    
    def test_student_class_sorting(self):
        """Тест сортировки объектов Student по GPA"""
        students = [
            Student("Bob", 3.2),
            Student("Alice", 3.8),
            Student("Charlie", 3.5),
            Student("Diana", 3.9),
            Student("Eve", 3.1)
        ]
        sorter = BogoSort(students)
        result = sorter.sort()
        
        # Проверяем что отсортировано по GPA
        expected_gpas = [3.1, 3.2, 3.5, 3.8, 3.9]
        actual_gpas = [s.gpa for s in result]
        self.assertEqual(actual_gpas, expected_gpas)
        self.assertTrue(sorter.is_sorted())
        
        # Проверяем что имена соответствуют GPA
        expected_names = ["Eve", "Bob", "Charlie", "Alice", "Diana"]
        actual_names = [s.name for s in result]
        self.assertEqual(actual_names, expected_names)
    
    def test_book_class_sorting(self):
        """Тест сортировки объектов Book по году издания"""
        books = [
            Book("1984", 1949),
            Book("Brave New World", 1932),
            Book("Fahrenheit 451", 1953),
            Book("Animal Farm", 1945),
            Book("We", 1924)
        ]
        sorter = BogoSort(books)
        result = sorter.sort()
        
        # Проверяем что отсортировано по году
        expected_years = [1924, 1932, 1945, 1949, 1953]
        actual_years = [b.year for b in result]
        self.assertEqual(actual_years, expected_years)
        self.assertTrue(sorter.is_sorted())
        
        # Проверяем что названия соответствуют годам
        expected_titles = ["We", "Brave New World", "Animal Farm", "1984", "Fahrenheit 451"]
        actual_titles = [b.title for b in result]
        self.assertEqual(actual_titles, expected_titles)
    
    def test_mixed_objects_same_class(self):
        """Тест сортировки смешанных объектов одного класса"""
        items = [
            Product("Cheap", 10.0),
            Product("Medium", 50.0),
            Product("Expensive", 100.0)
        ]
        sorter = BogoSort(items)
        result = sorter.sort()
        
        expected_prices = [10.0, 50.0, 100.0]
        actual_prices = [p.price for p in result]
        self.assertEqual(actual_prices, expected_prices)
        self.assertTrue(sorter.is_sorted())
    
    def test_get_array_method(self):
        """Тест метода get_array"""
        original = [3, 1, 2]
        sorter = BogoSort(original)
        array_copy = sorter.get_array()
        
        self.assertEqual(array_copy, [3, 1, 2])
        self.assertIsNot(array_copy, original)  # Должна возвращаться копия
    
    def test_set_array_method(self):
        """Тест метода set_array"""
        sorter = BogoSort([1, 2, 3])
        sorter.set_array([3, 2, 1])
        result = sorter.sort()
        
        self.assertEqual(result, [1, 2, 3])
        self.assertTrue(sorter.is_sorted())
    
    def test_str_representation(self):
        """Тест строкового представления"""
        sorter = BogoSort([3, 1, 2])
        str_repr = str(sorter)
        
        self.assertIn("BogoSort", str_repr)
        self.assertIn("[3, 1, 2]", str_repr)
        self.assertIn("sorted=False", str_repr)
        
        # После сортировки
        sorter.sort()
        str_repr_sorted = str(sorter)
        self.assertIn("sorted=True", str_repr_sorted)
    
    def test_original_array_unchanged(self):
        """Тест что исходный массив не изменяется"""
        original = [3, 1, 2]
        sorter = BogoSort(original)
        result = sorter.sort()
        
        self.assertEqual(original, [3, 1, 2])  # Исходный не изменился
        self.assertEqual(result, [1, 2, 3])    # Результат отсортирован
    
    def test_shuffle_method(self):
        """Тест метода shuffle"""
        sorter = BogoSort([1, 2, 3, 4, 5])
        original = sorter.get_array()
        sorter.shuffle()
        shuffled = sorter.get_array()
        
        # Массив должен измениться (с высокой вероятностью)
        self.assertNotEqual(original, shuffled)
        # Но содержать те же элементы
        self.assertEqual(sorted(original), sorted(shuffled))
    
    def test_is_sorted_method(self):
        """Тест метода is_sorted"""
        sorted_sorter = BogoSort([1, 2, 3])
        unsorted_sorter = BogoSort([3, 1, 2])
        
        self.assertTrue(sorted_sorter.is_sorted())
        self.assertFalse(unsorted_sorter.is_sorted())

if __name__ == '__main__':
    unittest.main(verbosity=2)