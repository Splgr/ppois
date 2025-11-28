class NeighborIterator:
    def __init__(self, graph, vertex, index=0):
        self._graph = graph
        self._vertex = vertex
        self._current_index = index
        self._start_idx = graph._start[vertex]
        self._end_idx = graph._start[vertex + 1]
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._current_index >= (self._end_idx - self._start_idx):
            raise StopIteration
        neighbor = self._graph._ends[self._start_idx + self._current_index]
        self._current_index += 1
        return neighbor
    
    def __eq__(self, other):
        if not isinstance(other, NeighborIterator):
            return False
        return (self._graph is other._graph and 
               self._vertex == other._vertex and 
               self._current_index == other._current_index)
    
    def __ne__(self, other):
        return not self.__eq__(other)