# Course: CS261 - Data Structures
# Author: Alexandra Fren
# Assignment: Six (Final)
# Description: This program creates a directed graph with an adjacency matrix, with methods to add a vertex or edge, remove an edge, get
# all vertices or edges, check if provided nodes have a valid path between them, do a dfs or bfs, check for cycles using
# bfs, and performs dijkstra calculations using a priority queue from heapq

from collections import deque
import heapq

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ---------------------------------------------------------------------------------------- #
    # Functions above this line were provided, below this line we're created as the assignment #
    # ---------------------------------------------------------------------------------------- #

    def add_vertex(self) -> int:
        """
        Add new vertex to the graph if not already present in the graph
        """
        counter = 0
        new_list = [0]
        while counter < self.v_count:
            self.adj_matrix[counter].append(0)
            new_list.append(0)
            counter += 1
        self.adj_matrix.append(new_list)
        self.v_count += 1
        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Add edge to the graph if valid inputs
        """
        if src > self.v_count - 1 or dst > self.v_count - 1 or weight < 0 or src == dst or src < 0 or dst < 0:
            return
        else:
            self.adj_matrix[src][dst] = weight
            return

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Remove edge from the graph
        """
        if src > self.v_count - 1 or dst > self.v_count - 1 or src == dst or src < 0 or dst < 0:
            return
        else:
            self.adj_matrix[src][dst] = 0
            return

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        counter = 0
        return_list = []
        while counter < self.v_count:
            return_list.append(counter)
            counter += 1
        return return_list

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        edge_list = []
        inner_counter = 0
        outer_counter = 0
        while outer_counter < self.v_count:
            while inner_counter < self.v_count:
                if self.adj_matrix[outer_counter][inner_counter] > 0:
                    edge_list.append((outer_counter, inner_counter, self.adj_matrix[outer_counter][inner_counter]))
                inner_counter += 1
            inner_counter = 0
            outer_counter += 1
        return edge_list

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        if len(path) == 0:
            return True
        else:
            counter = 0
            for i in path:
                if i >= self.v_count:
                    return False
                if counter == len(path) - 1:
                    # reached the end
                    return True
                else:
                    check_val = path[counter + 1]
                    if self.adj_matrix[path[counter]][check_val] == 0:
                        return False
                counter += 1

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order (see sort method used)
        """
        if v_start >= self.v_count:
            return []
        visitors = list()
        stack = deque()
        stack.append(v_start)
        while stack:
            v = stack.pop()
            if v == v_end:
                visitors.append(v)
                stack = deque()
            if v not in visitors:
                visitors.append(v)
                counter = 0
                holder = []
                while counter < self.v_count:
                    if self.adj_matrix[v][counter] > 0:
                        holder.append(counter)
                    counter += 1
                holder.sort(reverse=True)
                for i in holder:
                    stack.append(i)
        return visitors

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order (see sort method used)
        """
        if v_start >= self.v_count:
            return []
        h = deque()
        visitors = list()
        h.append(v_start)
        while h:
            v = h.popleft()
            if v == v_end:
                visitors.append(v)
                h = []
            if v not in visitors:
                visitors.append(v)
                counter = 0
                holder = []
                while counter < self.v_count:
                    if self.adj_matrix[v][counter] > 0:
                        holder.append(counter)
                    counter += 1
                holder.sort()
                for i in holder:
                    h.append(i)
        return visitors

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
        if len(self.get_vertices()) == 0 or len(self.get_vertices()) == 1:
            return False
        for index in range(self.v_count):
            reachable = []
            stack = [self.get_vertices()[index]]
            while stack:
                v = stack.pop()
                if v not in reachable:
                    reachable.append(v)
                for j in range(self.v_count):
                    if j not in reachable and self.adj_matrix[v][j] > 0:
                        stack.append(j)
                    if j in reachable and self.adj_matrix[v][j] > 0:
                        if v in self.bfs(j):
                            return True
        return False

    def dijkstra(self, src: int) -> []:
        """
        Performs calculations for the shortest path between each vertex in matrix
        """
        visited = {}
        heap = []
        distances = {}
        for i in self.get_vertices():
            # default should be inf if the vertex is not reachable, value will be check to see if its less later
            distances[i] = float('inf')
        # push the src value, with a priority 0 to the heap
        heapq.heapify(heap)
        heapq.heappush(heap, (0, src))
        while heap:
            v = heapq.heappop(heap)
            # d is the distance/priority of the popped value
            d = v[0]
            v = v[1]
            if v not in visited:
                visited[v] = d
            for j in range(self.v_count):
                total_distance = d + self.adj_matrix[v][j]
                if self.adj_matrix[v][j] > 0 and j not in visited and total_distance < distances[j]:
                    distances[j] = total_distance
                    heapq.heappush(heap, (total_distance, j))
        return_val = []
        for i in self.get_vertices():
            if i in visited:
                return_val.append(visited[i])
            else:
                return_val.append(float('inf'))
        return return_val


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
