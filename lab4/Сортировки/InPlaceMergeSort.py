from typing import TypeVar, Generic

T = TypeVar('T')

class InPlaceMergeSort(Generic[T]):
    """
    In-place merge sort для любого списка объектов с поддержкой операторов сравнения
    Сортирует оригинальный массив без создания копий и без дополнительной памяти
    """
    
    def sort(self, arr: list[T], start: int = 0, end: int = None) -> None:
        """Основной метод сортировки"""
        if end is None:
            end = len(arr) - 1
        
        if start < end:
            mid = (start + end) // 2
            
            # Рекурсивно сортируем левую и правую половины
            self.sort(arr, start, mid)
            self.sort(arr, mid + 1, end)
            
            # In-place слияние отсортированных половин
            self._merge_inplace(arr, start, mid, end)
    
    def _merge_inplace(self, arr: list[T], start: int, mid: int, end: int) -> None:
        """In-place слияние двух отсортированных подмассивов без дополнительной памяти"""
        left = start
        right = mid + 1
        
        while left <= mid and right <= end:
            # Если элемент слева меньше или равен - всё ок, двигаем левый указатель
            if arr[left] <= arr[right]:
                left += 1
            else:
                # Сохраняем элемент справа и сдвигаем элементы
                temp = arr[right]
                index = right
                
                # Сдвигаем все элементы от left до right-1 вправо
                while index > left:
                    arr[index] = arr[index - 1]
                    index -= 1
                
                # Вставляем сохранённый элемент на место left
                arr[left] = temp
                
                # Обновляем указатели
                left += 1
                mid += 1
                right += 1
    
    def is_sorted(self, arr: list[T]) -> bool:
        """Проверяет, отсортирован ли массив"""
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))