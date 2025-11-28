class VertexEdgeIterator:
    def __init__(self, graph, vertex, edge_index):
        self._graph = graph
        self._vertex = vertex
        self._current_index = edge_index
        self._neighbors = graph._get_neighbors_list(vertex)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._current_index >= len(self._neighbors):
            raise StopIteration
        neighbor = self._neighbors[self._current_index]
        u, v = min(self._vertex, neighbor), max(self._vertex, neighbor)
        result = (u, v)
        self._current_index += 1
        return result
    
    def prev(self):
        if self._current_index <= 0:
            raise StopIteration
        self._current_index -= 1
        neighbor = self._neighbors[self._current_index]
        u, v = min(self._vertex, neighbor), max(self._vertex, neighbor)
        return (u, v)
    
    def __eq__(self, other):
        if not isinstance(other, VertexEdgeIterator):
            return False
        return (self._graph is other._graph and 
               self._vertex == other._vertex and 
               self._current_index == other._current_index)
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def dereference(self):
        if self._current_index < 0 or self._current_index >= len(self._neighbors):
            raise IndexError("Iterator out of range")
        neighbor = self._neighbors[self._current_index]
        u, v = min(self._vertex, neighbor), max(self._vertex, neighbor)
        return (u, v)
