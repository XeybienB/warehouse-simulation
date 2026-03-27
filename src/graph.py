
import heapq


class WarehouseGraph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, node1, node2, weight):
        if node1 not in self.graph:
            self.graph[node1] = []
        if node2 not in self.graph:
            self.graph[node2] = []

        self.graph[node1].append((node2, weight))
        self.graph[node2].append((node1, weight))

    def dijkstra(self, start, end):
        pq = [(0, start, [])]
        visited = set()

        while pq:
            cost, node, path = heapq.heappop(pq)

            if node in visited:
                continue

            visited.add(node)
            path = path + [node]

            if node == end:
                return cost, path

            for neighbor, weight in self.graph.get(node, []):
                if neighbor not in visited:
                    heapq.heappush(pq, (cost + weight, neighbor, path))

        return float("inf"), []