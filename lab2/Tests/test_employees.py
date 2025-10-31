import unittest
from datetime import datetime
from Manager import Manager
from SalesRepresentative import SalesRepresentative
from SimplePasswordValidator import SimplePasswordValidator

class TestManagerUnit(unittest.TestCase):

    def setUp(self):
        self.manager = Manager(
            "Анна Петрова", "Менеджер", 50000.0, "EMP001", 
            datetime(2020, 1, 1), "Продажи", 10, 100000.0
        )

    def test_manager_creation(self):
        self.assertEqual(self.manager.name, "Анна Петрова")
        self.assertEqual(self.manager.department, "Продажи")
        self.assertEqual(self.manager.team_size, 10)
        self.assertEqual(self.manager.budget, 100000.0)

    def test_manager_attend_training(self):
        initial_salary = self.manager.salary
        self.manager.attend_training()
        self.assertEqual(self.manager.salary, initial_salary + 1000)

    def test_manager_allocate_budget(self):
        initial_budget = self.manager.budget
        self.manager.allocate_budget(5000.0)
        self.assertEqual(self.manager.budget, initial_budget - 5000.0)

class TestSalesRepresentativeUnit(unittest.TestCase):
    
    def setUp(self):
        self.sales_rep = SalesRepresentative(
            "Сергей Сидоров", "Продавец", 30000.0, "EMP002",
            datetime(2021, 1, 1), 500000.0
        )

    def test_sales_rep_creation(self):
        self.assertEqual(self.sales_rep.name, "Сергей Сидоров")
        self.assertEqual(self.sales_rep.sales_quota, 500000.0)

    def test_sales_rep_attend_training(self):
        initial_salary = self.sales_rep.salary
        self.sales_rep.attend_training()
        self.assertEqual(self.sales_rep.salary, initial_salary + 500)