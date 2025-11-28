import unittest
from WirthGraph import WirthGraph
from Product import Product
from Student import Student
from Book import Book

class TestWirthGraph(unittest.TestCase):
    
    def setUp(self):
        """Создание тестового графа перед каждым тестом"""
        self.graph = WirthGraph[str](5)  # Граф для строковых данных
        for i in range(5):
            self.graph.set_vertex_data(i, f"City_{i}")
        
        # Создаем структуру графа: 0-1-2-3-4 (линия)
        self.graph.add_edge(0, 1)
        self.graph.add_edge(1, 2)
        self.graph.add_edge(2, 3)
        self.graph.add_edge(3, 4)
        self.graph.add_edge(0, 2)
    
    def test_01_basic_properties(self):
        """Тест основных свойств графа"""
        self.assertFalse(self.graph.empty())
        self.assertEqual(self.graph.vertex_count(), 5)
        self.assertEqual(self.graph.edge_count(), 5)
    
    def test_02_vertex_operations(self):
        """Тест операций с вершинами"""
        # Проверка существования вершин
        self.assertTrue(self.graph.has_vertex(0))
        self.assertTrue(self.graph.has_vertex(4))
        self.assertFalse(self.graph.has_vertex(5))
        self.assertFalse(self.graph.has_vertex(-1))
        
        # Проверка данных вершин
        self.assertEqual(self.graph.get_vertex_data(0), "City_0")
        self.graph.set_vertex_data(1, "Updated_City")
        self.assertEqual(self.graph.get_vertex_data(1), "Updated_City")
        
        # Добавление новой вершины
        new_vertex = self.graph.add_vertex("New_City")
        self.assertEqual(new_vertex, 5)
        self.assertEqual(self.graph.vertex_count(), 6)
        self.assertEqual(self.graph.get_vertex_data(5), "New_City")
    
    def test_03_edge_operations(self):
        """Тест операций с рёбрами"""
        # Проверка существования рёбер
        self.assertTrue(self.graph.has_edge(0, 1))
        self.assertTrue(self.graph.has_edge(1, 0))  # Неориентированность
        self.assertTrue(self.graph.has_edge(0, 2))
        self.assertFalse(self.graph.has_edge(0, 3))
        self.assertFalse(self.graph.has_edge(5, 0))  # Несуществующая вершина
        
        # Удаление ребра
        self.assertTrue(self.graph.remove_edge(0, 1))
        self.assertFalse(self.graph.has_edge(0, 1))
        self.assertEqual(self.graph.edge_count(), 4)
        
        # Попытка удалить несуществующее ребро
        self.assertFalse(self.graph.remove_edge(0, 3))
    
    def test_04_degree_calculation(self):
        """Тест вычисления степеней"""
        # Степени вершин
        self.assertEqual(self.graph.vertex_degree(0), 2)  # Связана с 1 и 2
        self.assertEqual(self.graph.vertex_degree(1), 2)  # Связана с 0 и 2
        self.assertEqual(self.graph.vertex_degree(4), 1)  # Связана только с 3
        self.assertEqual(self.graph.vertex_degree(5), 0)  # Несуществующая вершина
        
        # Степени рёбер
        self.assertEqual(self.graph.edge_degree((0, 1)), 2)  # (2 + 2 - 2) = 2
        self.assertEqual(self.graph.edge_degree((3, 4)), 1)  # (2 + 1 - 2) = 1
        self.assertEqual(self.graph.edge_degree((0, 3)), 0)  # Несуществующее ребро
    
    def test_05_vertex_removal(self):
        """Тест удаления вершины"""
        # Удаляем вершину 2
        self.assertTrue(self.graph.remove_vertex(2))
        self.assertEqual(self.graph.vertex_count(), 4)

        self.assertFalse(self.graph.has_edge(1, 2))
        self.assertFalse(self.graph.has_edge(0, 2))
        
    
    def test_06_comparison_operators(self):
        """Тест операторов сравнения"""
        graph1 = WirthGraph[int](3, [(0,1), (1,2)])
        graph2 = WirthGraph[int](3, [(0,1), (1,2)])
        graph3 = WirthGraph[int](2, [(0,1)])
        graph4 = WirthGraph[int](3, [(0,1)])
        
        # Равенство
        self.assertEqual(graph1, graph2)
        self.assertNotEqual(graph1, graph3)
        
        # Сравнение
        self.assertLess(graph3, graph1)    # 2 вершины < 3 вершин
        self.assertLess(graph4, graph1)    # 1 ребро < 2 рёбер (при равных вершинах)
        self.assertGreater(graph1, graph3)
        self.assertLessEqual(graph1, graph2)
        self.assertGreaterEqual(graph1, graph2)
    
    def test_07_vertex_iterators(self):
        """Тест итераторов вершин"""
        # Прямой обход
        vertices = list(self.graph.vertices_begin())
        self.assertEqual(vertices, [0, 1, 2, 3, 4])
        
        # Обратный обход
        reverse_vertices = list(self.graph.vertices_rbegin())
        self.assertEqual(reverse_vertices, [4, 3, 2, 1, 0])
        
        # Двунаправленность
        it = self.graph.vertices_begin()
        self.assertEqual(next(it), 0)
        self.assertEqual(next(it), 1)
        self.assertEqual(it.prev(), 1)  # Можем вернуться назад
    
    def test_08_edge_iterators(self):
        """Тест итераторов рёбер"""
        # Прямой обход рёбер
        edges = list(self.graph.edges_begin())
        expected_edges = [(0,1), (1,2), (2,3), (3,4), (0,2)]
        self.assertEqual(edges, expected_edges)
        
        # Обратный обход рёбер
        reverse_edges = list(self.graph.edges_rbegin())
        self.assertEqual(reverse_edges, list(reversed(expected_edges)))
    
    def test_09_neighbor_iterators(self):
        """Тест итераторов смежных вершин"""
        # Прямой обход соседей вершины 1
        neighbors = list(self.graph.neighbors_begin(1))
        self.assertEqual(sorted(neighbors), [0, 2])  # Соседи 1: 0 и 2
        
        # Обратный обход соседей вершины 1
        reverse_neighbors = list(self.graph.neighbors_rbegin(1))
        self.assertEqual(reverse_neighbors, [2, 0])  # В обратном порядке
        
        # Однонаправленность - нет метода prev()
        it = self.graph.neighbors_begin(1)
        self.assertTrue(hasattr(it, '__next__'))
        self.assertFalse(hasattr(it, 'prev'))  # Однонаправленный!
    
    def test_10_vertex_edge_iterators(self):
        """Тест итераторов инцидентных рёбер"""
        # Рёбра, инцидентные вершине 1
        incident_edges = list(self.graph.vertex_edges_begin(1))
        expected_edges = [(0,1), (1,2)]  # Рёбра (0,1) и (1,2)
        self.assertEqual(incident_edges, expected_edges)
        
        # Обратный обход
        reverse_incident = list(self.graph.vertex_edges_rbegin(1))
        self.assertEqual(reverse_incident, list(reversed(expected_edges)))
    
    def test_11_iterator_removal(self):
        """Тест удаления по итераторам"""
        # Устанавливаем уникальные данные для каждой вершины
        for i in range(5):
            self.graph.set_vertex_data(i, f"Unique_{i}")
        
        vertex_it = self.graph.vertices_begin()
        vertex_to_remove = vertex_it.dereference()  # = 0
        removed_data = self.graph.get_vertex_data(vertex_to_remove)  # "Unique_0"
        
        new_it = self.graph.remove_vertex_by_iterator(vertex_it)
        
        # Проверяем, что данных удаленной вершины больше нет
        remaining_data = [self.graph.get_vertex_data(v) for v in self.graph.vertices_begin()]
        self.assertNotIn(removed_data, remaining_data)  # "Unique_0" удален
    
    def test_12_error_handling(self):
        """Тест обработки ошибок"""
        # Обращение к несуществующей вершине
        with self.assertRaises(IndexError):
            self.graph.get_vertex_data(10)
        
        with self.assertRaises(IndexError):
            self.graph.set_vertex_data(10, "Invalid")
        
        # Добавление ребра с несуществующей вершиной
        with self.assertRaises(IndexError):
            self.graph.add_edge(0, 10)
        
        # Итераторы для несуществующей вершины
        with self.assertRaises(IndexError):
            self.graph.neighbors_begin(10)
    
    def test_13_clear_and_empty(self):
        """Тест очистки графа"""
        self.assertFalse(self.graph.empty())
        self.graph.clear()
        self.assertTrue(self.graph.empty())
        self.assertEqual(self.graph.vertex_count(), 0)
        self.assertEqual(self.graph.edge_count(), 0)
    
    def test_14_string_representation(self):
        """Тест строкового представления"""
        str_repr = str(self.graph)
        self.assertIn("WirthGraph(vertices=5, edges=5)", str_repr)
        self.assertIn("Vertex 0", str_repr)
        self.assertIn("City_0", str_repr)
    
    def test_15_generic_type_support(self):
        """Тест поддержки generic-типов"""
        # Граф с целыми числами
        int_graph = WirthGraph[int](3)
        int_graph.set_vertex_data(0, 100)
        self.assertEqual(int_graph.get_vertex_data(0), 100)
        
        # Граф со словарями
        dict_graph = WirthGraph[dict](2)
        dict_graph.set_vertex_data(0, {"name": "test"})
        self.assertEqual(dict_graph.get_vertex_data(0), {"name": "test"})
    
    def test_16_product_class_storage(self):
        """Тест хранения объектов Product в вершинах"""
        product_graph = WirthGraph[Product](4)

        products = [
            Product("Laptop", 999.99),
            Product("Mouse", 25.50),
            Product("Keyboard", 75.00),
            Product("Monitor", 299.99)
        ]
        
        for i, product in enumerate(products):
            product_graph.set_vertex_data(i, product)

        self.assertEqual(product_graph.get_vertex_data(0).name, "Laptop")
        self.assertEqual(product_graph.get_vertex_data(0).price, 999.99)
        self.assertEqual(product_graph.get_vertex_data(1).name, "Mouse")

        self.assertLess(product_graph.get_vertex_data(1), product_graph.get_vertex_data(0))  # 25.50 < 999.99
        self.assertGreater(product_graph.get_vertex_data(0), product_graph.get_vertex_data(1))
    
    def test_17_student_class_storage(self):
        """Тест хранения объектов Student в вершинах"""
        student_graph = WirthGraph[Student](3)
        
        students = [
            Student("Alice", 3.8),
            Student("Bob", 3.2),
            Student("Charlie", 3.9)
        ]
        
        for i, student in enumerate(students):
            student_graph.set_vertex_data(i, student)

        student_graph.add_edge(0, 1)
        student_graph.add_edge(1, 2)

        self.assertEqual(student_graph.get_vertex_data(0).name, "Alice")
        self.assertEqual(student_graph.get_vertex_data(0).gpa, 3.8)
        self.assertEqual(student_graph.vertex_degree(1), 2)
  
        self.assertLess(student_graph.get_vertex_data(1), student_graph.get_vertex_data(0))
    
    def test_18_book_class_storage(self):
        """Тест хранения объектов Book в вершинах"""
        book_graph = WirthGraph[Book](5)
        
        books = [
            Book("1984", 1949),
            Book("Brave New World", 1932),
            Book("Fahrenheit 451", 1953),
            Book("Animal Farm", 1945),
            Book("We", 1924)
        ]
        
        for i, book in enumerate(books):
            book_graph.set_vertex_data(i, book)
        
        # Создаем граф цитирования (какие книги ссылаются на какие)
        book_graph.add_edge(0, 1)  # 1984 -> Brave New World
        book_graph.add_edge(0, 3)  # 1984 -> Animal Farm
        book_graph.add_edge(1, 4)  # Brave New World -> We
        book_graph.add_edge(2, 0)  # Fahrenheit 451 -> 1984
        
        # Проверяем данные
        self.assertEqual(book_graph.get_vertex_data(0).title, "1984")
        self.assertEqual(book_graph.get_vertex_data(0).year, 1949)
        
        # Проверяем связи
        self.assertEqual(book_graph.vertex_degree(0), 3)  # 1984 связана с 3 книгами
        
        # Проверяем сравнение по году издания
        self.assertLess(book_graph.get_vertex_data(4), book_graph.get_vertex_data(1))  # 1924 < 1932
    
    def test_19_mixed_operations_with_classes(self):
        """Тест смешанных операций с объектами классов"""
        graph = WirthGraph[Product](3)
        
        # Добавляем продукты
        graph.set_vertex_data(0, Product("Phone", 500.0))
        graph.set_vertex_data(1, Product("Tablet", 300.0))
        graph.set_vertex_data(2, Product("Watch", 200.0))
        
        # Создаем связи (совместимые устройства)
        graph.add_edge(0, 1)  # Phone - Tablet
        graph.add_edge(1, 2)  # Tablet - Watch
        
        # Проверяем итераторы с объектами
        vertices_data = [graph.get_vertex_data(v) for v in graph.vertices_begin()]
        self.assertEqual(len(vertices_data), 3)
        self.assertTrue(all(isinstance(data, Product) for data in vertices_data))
        
        # Проверяем соседей
        neighbors = list(graph.neighbors_begin(1))
        self.assertEqual(len(neighbors), 2)  # Tablet связан с Phone и Watch
        
        # Удаляем вершину и проверяем целостность
        graph.remove_vertex(1)
        self.assertEqual(graph.vertex_count(), 2)
        
        # Проверяем, что оставшиеся данные корректны
        remaining_data = [graph.get_vertex_data(v) for v in graph.vertices_begin()]
        self.assertEqual(len(remaining_data), 2)
        self.assertTrue(all(isinstance(data, Product) for data in remaining_data))
    
    def test_20_string_representation_with_classes(self):
        """Тест строкового представления с объектами классов"""
        graph = WirthGraph[Student](2)
        graph.set_vertex_data(0, Student("Alice", 3.8))
        graph.set_vertex_data(1, Student("Bob", 3.2))
        graph.add_edge(0, 1)
        
        str_repr = str(graph)
        
        # Проверяем, что строковое представление содержит информацию о студентах
        self.assertIn("Student('Alice', GPA: 3.8)", str_repr)
        self.assertIn("Student('Bob', GPA: 3.2)", str_repr)
        self.assertIn("WirthGraph(vertices=2, edges=1)", str_repr)

    def test_21_book_comparison_operators(self):
        """Тест операторов сравнения для Book - покрывает пропущенные строки в Book.py"""
        book1 = Book("Book1", 2000)
        book2 = Book("Book2", 2010)
        book3 = Book("Book3", 2000)
        
        # Тест __lt__ (строка 16-18 в Book.py)
        self.assertTrue(book1 < book2)  # 2000 < 2010
        self.assertFalse(book2 < book1)
        self.assertFalse(book1 < book3)  # равные года
        
        # Тест __eq__ (строка 13 в Book.py)  
        self.assertTrue(book1 == book3)  # оба 2000
        self.assertFalse(book1 == book2)
        
        # Тест __repr__ (строка 21 в Book.py)
        self.assertEqual(repr(book1), "Book('Book1', 2000)")

    def test_22_vertex_edge_iterator_edge_cases(self):
        """Тест крайних случаев VertexEdgeIterator - покрывает пропущенные строки"""
        graph = WirthGraph[str](3)
        
        # Тест для изолированной вершины (без рёбер)
        iterator = graph.vertex_edges_begin(0)
        
        # Тестируем методы для пустого итератора (строки 21-26, 29-31)
        end_iterator = graph.vertex_edges_end(0)
        self.assertTrue(iterator == end_iterator)
        
        # Добавляем ребро
        graph.add_edge(0, 1)
        iterator = graph.vertex_edges_begin(0)
        
        # Тестируем dereference() (строки 39-43)
        edge = iterator.dereference()
        self.assertEqual(edge, (0, 1))
        
        # Тестируем next() и проверяем конец (строки 36)
        next(iterator)
        self.assertTrue(iterator == graph.vertex_edges_end(0))

    def test_23_reverse_vertex_edge_iterator_edge_cases(self):
        """Тест ReverseVertexEdgeIterator - покрывает пропущенные строки"""
        graph = WirthGraph[str](3)
        
        # Тест для изолированной вершины
        iterator = graph.vertex_edges_rbegin(0)
        
        # Тестируем методы для пустого итератора (строки 22-27, 30-32)
        rend_iterator = graph.vertex_edges_rend(0)
        self.assertTrue(iterator == rend_iterator)
        
        # Добавляем рёбра
        graph.add_edge(0, 1)
        graph.add_edge(0, 2)
        
        iterator = graph.vertex_edges_rbegin(0)
        
        # Тестируем dereference() (строки 40-44)
        edge = iterator.dereference()
        self.assertEqual(edge, (0, 2))
        
        # Тестируем next() (строки 37)
        next_edge = next(iterator)
        self.assertEqual(next_edge, (0, 2))

    def test_24_edge_iterator_comprehensive(self):
        """Тест EdgeIterator - покрывает пропущенные строки"""
        graph = WirthGraph[str](3, [(0,1), (1,2)])
        
        edge_it = graph.edges_begin()
        
        # Тестируем dereference() (строки 17-20)
        first_edge = edge_it.dereference()
        self.assertEqual(first_edge, (0, 1))

        next_edge = next(edge_it)
        self.assertEqual(next_edge, (0, 1))
        
        # Тестируем prev() (строки 28)
        prev_edge = edge_it.prev()
        self.assertEqual(prev_edge, (0, 1))
        
        # Тестируем сравнение итераторов (строки 31-33)
        it1 = graph.edges_begin()
        it2 = graph.edges_begin()
        self.assertTrue(it1 == it2)
        self.assertFalse(it1 != it2)

    def test_25_reverse_edge_iterator_comprehensive(self):
        """Тест ReverseEdgeIterator - покрывает пропущенные строки"""
        graph = WirthGraph[str](3, [(0,1), (1,2)])
        
        rev_it = graph.edges_rbegin()
        
        # Тестируем dereference() (строки 18-21)
        last_edge = rev_it.dereference()
        self.assertEqual(last_edge, (1, 2))
        
        # Тестируем next() (строки 24-26)
        next_edge = next(rev_it)
        self.assertEqual(next_edge, (1, 2))
        
        # Тестируем prev() (строки 29)
        prev_edge = rev_it.prev()
        self.assertEqual(prev_edge, (1, 2))
        
        # Тестируем сравнение (строки 32-34)
        it1 = graph.edges_rbegin()
        it2 = graph.edges_rbegin()
        self.assertTrue(it1 == it2)


if __name__ == '__main__':
    unittest.main(verbosity=2)