from copy import deepcopy

class Graph:
    def __init__(self, lis1, lis2):
        self.graph = []
        self.revers_graph = []
        self.lis_aux_cri = []
        self.lis_rev = []
        self.lis_criticos = []
        self.in_list_nodes = []
        self.in_list_edges = []
        self.res = []

        for i in range(1, len(lis1)+1):
            self.in_list_nodes.append(i)

        self.in_list_edges = deepcopy(lis2)

    def build_graph(self, lis_nodes, lis_edges):
        self.graph = {i: [] for i in lis_nodes}
        for v, u, cost in lis_edges:
            self.graph[v].append((u, cost))
        return self.graph

    def bellman_ford(self, source, target):
        dist = {node: float('inf') for node in self.graph}
        predecessor = {node: None for node in self.graph}
        dist[source] = 0

        for _ in range(len(self.graph) - 1):
            for u in self.graph:
                for v, cost in self.graph[u]:
                    if dist[u] + cost < dist[v]:
                        dist[v] = dist[u] + cost
                        predecessor[v] = u

        for u in self.graph:
            for v, cost in self.graph[u]:
                if dist[u] + cost < dist[v]:
                    return None, None, True

        path = []
        current = target
        while current is not None:
            path.append(current)
            current = predecessor[current]
        path.reverse()

        return dist, path, False

    def run(self):
        g = Graph.build_graph(self, self.in_list_nodes, self.in_list_edges)
        
        source = self.in_list_nodes[0]
        target = self.in_list_nodes[-1]
        
        distances, path, has_negative_cycle = self.bellman_ford(source, target)
        
        if has_negative_cycle:
            return None, None, True
        
        if path:
            print(f"Menor caminho do nó {source} ao nó {target}: {path}")
        return distances, path, False
