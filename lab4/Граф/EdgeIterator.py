class EdgeIterator:
    def __init__(self, graph, index):
        self._graph = graph
        self._index = index
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index >= len(self._graph._edges):
            raise StopIteration
        result = self._graph._edges[self._index]
        self._index += 1
        return result
    
    def prev(self):
        if self._index <= 0:
            raise StopIteration
        self._index -= 1
        return self._graph._edges[self._index]
    
    def __eq__(self, other):
        if not isinstance(other, EdgeIterator):
            return False
        return self._graph is other._graph and self._index == other._index
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def dereference(self):
        if self._index < 0 or self._index >= len(self._graph._edges):
            raise IndexError("Iterator out of range")
        return self._graph._edges[self._index]