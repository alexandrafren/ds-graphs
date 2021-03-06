# Course: CS261 - Data Structures
# Author: Alexandra Fren
# Assignment: Six
# Description: This program creates an undirected graph, with methods to add a vertex or edge, remove a vertex or edge,
# get a list of all vertices or edges, do a dfs or bfs, check if a passed path is valid, check for cycles, and returns
# the count of connected components.

from collections import deque

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ----------------------------------------------------------------------------------- #
    # functions above line were provided, functions below were created for the assignment #
    # ----------------------------------------------------------------------------------- #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph if not already present in the graph
        """
        if v not in self.adj_list:
            self.adj_list[v] = []
        return
        
    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph if valid inputs
        """
        if u == v:
            return
        else:
            if u not in self.adj_list:
                self.add_vertex(u)
            if v not in self.adj_list:
                self.add_vertex(v)
            if v not in self.adj_list[u]:
                self.adj_list[u].append(v)
            if u not in self.adj_list[v]:
                self.adj_list[v].append(u)
            return

    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """
        if v in self.adj_list and u in self.adj_list:
            if u in self.adj_list[v]:
                self.adj_list[v].remove(u)
            if v in self.adj_list[u]:
                self.adj_list[u].remove(v)
        else:
            return

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        if v in self.adj_list:
            self.adj_list.pop(v)
            keys = self.adj_list.keys()
            for i in keys:
                if v in self.adj_list[i]:
                    self.adj_list[i].remove(v)
            return
        else:
            return

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        return list(self.adj_list.keys())

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        edge_list = []
        keys = self.adj_list.keys()
        for i in keys:
            l = self.adj_list[i]
            count = 0
            while count < len(l):
                pair1 = tuple((i, l[count]))
                pair2 = tuple((l[count], i))
                if pair1 not in edge_list and pair2 not in edge_list:
                    edge_list.append(pair1)
                count += 1
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
                if i not in self.adj_list:
                    return False
                if counter == len(path) - 1:
                    return True
                else:
                    check_val = path[counter + 1]
                    if check_val not in self.adj_list[i]:
                        return False
                counter += 1

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order (see sort method used)
        """
        if v_start not in self.adj_list:
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
                holder = list()
                for i in self.adj_list[v]:
                    if i not in visitors:
                        holder.append(i)
                    holder.sort(reverse=True)
                for i in holder:
                    stack.append(i)
        return visitors

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order (see sort method used)
        """
        if v_start not in self.adj_list:
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
                holder = []
                for i in self.adj_list[v]:
                    if i not in visitors:
                        holder.append(i)
                holder.sort()
                for i in holder:
                    h.append(i)
        return visitors

    def count_connected_components(self):
        """
        Return number of connected components in the graph
        """
        compare_lists = []
        for i in self.get_vertices():
            comp = sorted(self.dfs(i))
            if comp not in compare_lists:
                compare_lists.append(comp)
        return len(compare_lists)

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
        if len(self.get_vertices()) == 0 or len(self.get_vertices()) == 1:
            return False
        else:
            for index in range(len(self.get_vertices())):
                prev = self.get_vertices()[index]
                accessed = []
                s = [(prev, prev)]
                while s:
                    v = s.pop()
                    cur = v[0]
                    prev = v[1]
                    if cur not in accessed:
                        accessed.append(cur)
                    for i in sorted(self.adj_list[cur], reverse=True):
                        if i not in accessed:
                            s.append((i, cur))
                        if i in accessed and i != prev:
                            # eliminate possibility of loop
                            return True
            return False


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH')
    test_cases_2 = ('remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print("+_______________a ove SHOULD WORK")
    for case in test_cases_2:
        print(g)
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE')
    test_cases_2 = ('remove CA', 'remove EB', 'remove CE', 'remove DE')
    test_cases_3 = ('remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
    for case in test_cases_2:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
    for case in test_cases_3:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
