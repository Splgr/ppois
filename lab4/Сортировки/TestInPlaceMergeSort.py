import unittest
from Product import Product
from Student import Student
from Book import Book
from InPlaceMergeSort import InPlaceMergeSort


class TestInPlaceMergeSort(unittest.TestCase):
    
    def setUp(self):
        self.sorter = InPlaceMergeSort()
    
    def test_empty_list(self):
        arr = []
        self.sorter.sort(arr)
        self.assertEqual(arr, [])
    
    def test_single_element(self):
        arr = [5]
        self.sorter.sort(arr)
        self.assertEqual(arr, [5])
    
    def test_sorted_array(self):
        arr = [1, 2, 3, 4, 5]
        self.sorter.sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])
    
    def test_reverse_sorted_array(self):
        arr = [5, 4, 3, 2, 1]
        self.sorter.sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])
    
    def test_random_array(self):
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        self.sorter.sort(arr)
        self.assertEqual(arr, [1, 1, 2, 3, 4, 5, 6, 9])
    
    def test_duplicate_elements(self):
        arr = [5, 2, 5, 1, 2, 1]
        self.sorter.sort(arr)
        self.assertEqual(arr, [1, 1, 2, 2, 5, 5])


class TestInPlaceMergeSortWithCustomClasses(unittest.TestCase):
    
    def setUp(self):
        self.sorter = InPlaceMergeSort()
    
    def test_product_sort_by_price(self):
        products = [
            Product("Laptop", 1000),
            Product("Mouse", 25),
            Product("Keyboard", 75),
            Product("Monitor", 300)
        ]
        self.sorter.sort(products)
        
        self.assertEqual(products[0].price, 25)
        self.assertEqual(products[1].price, 75)
        self.assertEqual(products[2].price, 300)
        self.assertEqual(products[3].price, 1000)
    
    def test_student_sort_by_gpa(self):
        students = [
            Student("Alice", 3.8),
            Student("Bob", 3.9),
            Student("Charlie", 3.5),
            Student("Diana", 3.7)
        ]
        self.sorter.sort(students)
        
        self.assertEqual(students[0].gpa, 3.5)
        self.assertEqual(students[1].gpa, 3.7)
        self.assertEqual(students[2].gpa, 3.8)
        self.assertEqual(students[3].gpa, 3.9)
    
    def test_book_sort_by_year(self):
        books = [
            Book("1984", 1949),
            Book("Brave New World", 1932),
            Book("Fahrenheit 451", 1953)
        ]
        self.sorter.sort(books)
        
        self.assertEqual(books[0].year, 1932)
        self.assertEqual(books[1].year, 1949)
        self.assertEqual(books[2].year, 1953)


if __name__ == '__main__':
    unittest.main()