import random
from typing import TypeVar, Generic

T = TypeVar('T')

class BogoSort(Generic[T]):
    def __init__(self, arr: list[T] = None):
        self._arr = arr.copy() if arr else []
    
    def is_sorted(self) -> bool:
        """Проверяет, отсортирован ли массив"""
        return all(self._arr[i] <= self._arr[i + 1] for i in range(len(self._arr) - 1))
    
    def shuffle(self) -> None:
        """Перемешивает массив случайным образом"""
        random.shuffle(self._arr)
    
    def sort(self) -> list[T]:
        """Выполняет сортировку bogosort"""
        while not self.is_sorted():
            self.shuffle()
        return self._arr.copy()
    
    def get_array(self) -> list[T]:
        """Возвращает копию текущего массива"""
        return self._arr.copy()
    
    def set_array(self, arr: list[T]) -> None:
        """Устанавливает новый массив для сортировки"""
        self._arr = arr.copy()
    
    def __str__(self) -> str:
        return f"BogoSort(array={self._arr}, sorted={self.is_sorted()})"
