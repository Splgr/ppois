from typing import Generic, TypeVar
from VertexIterator import VertexIterator
from ReverseVertexIterator import ReverseVertexIterator
from EdgeIterator import EdgeIterator
from ReverseEdgeIterator import ReverseEdgeIterator
from VertexEdgeIterator import VertexEdgeIterator
from ReverseVertexEdgeIterator import ReverseVertexEdgeIterator
from NeighborIterator import NeighborIterator
from ReverseNeighborIterator import ReverseNeighborIterator

T = TypeVar('T')

class WirthGraph(Generic[T]):
    def __init__(self, vertex_count=0, edges=None):
        self._vertex_count = vertex_count
        self._vertex_data = [None] * vertex_count
        self._start = [0] * (vertex_count + 1) if vertex_count > 0 else [0]
        self._ends = []
        self._edges = []
        
        if edges:
            for edge in edges:
                u, v = edge
                self._edges.append((min(u, v), max(u, v)))

    def _build_arrays(self):
        if self._vertex_count == 0:
            return
            
        degree = [0] * self._vertex_count
        for u, v in self._edges:
            if u < 0 or u >= self._vertex_count or v < 0 or v >= self._vertex_count:
                raise IndexError("Vertex index out of range")
            degree[u] += 1
            degree[v] += 1
        
        self._start = [0] * (self._vertex_count + 1)
        for i in range(1, self._vertex_count + 1):
            self._start[i] = self._start[i - 1] + degree[i - 1]
        
        current_pos = self._start.copy()
        self._ends = [0] * (2 * len(self._edges))
        
        for u, v in self._edges:
            self._ends[current_pos[u]] = v
            current_pos[u] += 1
            self._ends[current_pos[v]] = u
            current_pos[v] += 1

    def __eq__(self, other):
        """Сравнение на равенство графов"""
        if not isinstance(other, WirthGraph):
            return False
        return (self._vertex_count == other._vertex_count and
                self._edges == other._edges and
                self._vertex_data == other._vertex_data)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        """Сравнение графов (по количеству вершин, затем рёбер)"""
        if not isinstance(other, WirthGraph):
            return NotImplemented
        if self._vertex_count != other._vertex_count:
            return self._vertex_count < other._vertex_count
        return len(self._edges) < len(other._edges)

    def __gt__(self, other):
        return other.__lt__(self)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def _get_neighbors_list(self, vertex):
        if vertex < 0 or vertex >= self._vertex_count:
            return []
        start_idx = self._start[vertex]
        end_idx = self._start[vertex + 1]
        return self._ends[start_idx:end_idx]

    # Основные методы контейнера
    def empty(self):
        return self._vertex_count == 0

    def clear(self):
        self._vertex_count = 0
        self._vertex_data = []
        self._start = [0]
        self._ends = []
        self._edges = []

    def vertex_count(self):
        return self._vertex_count

    def edge_count(self):
        return len(self._edges)

    def has_vertex(self, vertex):
        return 0 <= vertex < self._vertex_count

    def has_edge(self, u, v):
        if not self.has_vertex(u) or not self.has_vertex(v):
            return False
        return v in self._get_neighbors_list(u)

    def vertex_degree(self, vertex):
        if not self.has_vertex(vertex):
            return 0
        return self._start[vertex + 1] - self._start[vertex]

    def edge_degree(self, edge):
        u, v = edge
        if not self.has_edge(u, v):
            return 0
        return self.vertex_degree(u) + self.vertex_degree(v) - 2

    def add_vertex(self, data: T = None):
        self._vertex_count += 1
        self._vertex_data.append(data)
        self._start.append(self._start[-1] + 1)
        return self._vertex_count - 1

    def add_edge(self, u, v):
        if not self.has_vertex(u) or not self.has_vertex(v):
            raise IndexError("Vertex index out of range")
        if self.has_edge(u, v):
            return
        
        self._edges.append((min(u, v), max(u, v)))
        self._build_arrays()

    def remove_vertex(self, vertex):
        if not self.has_vertex(vertex):
            return False
        
        self._edges = [(u, v) for u, v in self._edges if u != vertex and v != vertex]
        
        new_edges = []
        for u, v in self._edges:
            new_u = u - 1 if u > vertex else u
            new_v = v - 1 if v > vertex else v
            new_edges.append((new_u, new_v))
        
        self._edges = new_edges
        self._vertex_count -= 1
        self._vertex_data.pop(vertex)
        self._build_arrays()
        return True

    def remove_edge(self, u, v):
        edge = (min(u, v), max(u, v))
        if edge in self._edges:
            self._edges.remove(edge)
            self._build_arrays()
            return True
        return False

    # Методы для работы с данными вершин
    def set_vertex_data(self, vertex, data: T):
        if not self.has_vertex(vertex):
            raise IndexError("Vertex index out of range")
        self._vertex_data[vertex] = data

    def get_vertex_data(self, vertex) -> T:
        if not self.has_vertex(vertex):
            raise IndexError("Vertex index out of range")
        return self._vertex_data[vertex]

    # Итераторы
    def vertices_begin(self):
        return VertexIterator(self, 0)
    
    def vertices_end(self):
        return VertexIterator(self, self._vertex_count)
    
    def edges_begin(self):
        return EdgeIterator(self, 0)
    
    def edges_end(self):
        return EdgeIterator(self, len(self._edges))
    
    def vertex_edges_begin(self, vertex):
        if not self.has_vertex(vertex):
            raise IndexError("Vertex index out of range")
        return VertexEdgeIterator(self, vertex, 0)
    
    def vertex_edges_end(self, vertex):
        if not self.has_vertex(vertex):
            raise IndexError("Vertex index out of range")
        return VertexEdgeIterator(self, vertex, len(self._get_neighbors_list(vertex)))
    
    def neighbors_begin(self, vertex):
        if not self.has_vertex(vertex):
            raise IndexError("Vertex index out of range")
        return NeighborIterator(self, vertex, 0)
    
    def neighbors_end(self, vertex):
        if not self.has_vertex(vertex):
            raise IndexError("Vertex index out of range")
        neighbor_count = self._start[vertex + 1] - self._start[vertex]
        return NeighborIterator(self, vertex, neighbor_count)

    # Обратные итераторы
    def vertices_rbegin(self):
        return ReverseVertexIterator(self, self._vertex_count - 1)
    
    def vertices_rend(self):
        return ReverseVertexIterator(self, -1)
    
    def edges_rbegin(self):
        return ReverseEdgeIterator(self, len(self._edges) - 1)
    
    def edges_rend(self):
        return ReverseEdgeIterator(self, -1)
    
    def vertex_edges_rbegin(self, vertex):
        if not self.has_vertex(vertex):
            raise IndexError("Vertex index out of range")
        return ReverseVertexEdgeIterator(self, vertex, len(self._get_neighbors_list(vertex)) - 1)
    
    def vertex_edges_rend(self, vertex):
        if not self.has_vertex(vertex):
            raise IndexError("Vertex index out of range")
        return ReverseVertexEdgeIterator(self, vertex, -1)
    
    def neighbors_rbegin(self, vertex):
        if not self.has_vertex(vertex):
            raise IndexError("Vertex index out of range")
        neighbor_count = self._start[vertex + 1] - self._start[vertex]
        return ReverseNeighborIterator(self, vertex, neighbor_count - 1)
    
    def neighbors_rend(self, vertex):
        if not self.has_vertex(vertex):
            raise IndexError("Vertex index out of range")
        return ReverseNeighborIterator(self, vertex, -1)

    # Удаление по итераторам
    def remove_vertex_by_iterator(self, it):
        vertex = it.dereference()
        self.remove_vertex(vertex)
        return VertexIterator(self, vertex)
    
    def remove_edge_by_iterator(self, it):
        edge = it.dereference()
        self.remove_edge(edge[0], edge[1])
        return EdgeIterator(self, it._index)

    def __str__(self):
        result = f"WirthGraph(vertices={self._vertex_count}, edges={len(self._edges)})\n"
        for v in range(self._vertex_count):
            neighbors = list(self.neighbors_begin(v))
            data = self.get_vertex_data(v)
            result += f"Vertex {v} (data: {data}): {neighbors}\n"
        return result
