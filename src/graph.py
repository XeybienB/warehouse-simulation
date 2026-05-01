import networkx as nx


class WarehouseLayout:
    def __init__(self):
        self.G = nx.Graph()
        edges = [
            ("Dock", "Aisle_A", 2),
            ("Dock", "Aisle_B", 4),
            ("Aisle_A", "Aisle_C", 3),
            ("Aisle_B", "Aisle_C", 1),
            ("Aisle_C", "Packing", 2),
            ("Aisle_A", "Packing", 5),
        ]
        for u, v, w in edges:
            self.G.add_edge(u, v, travel_time=w)

        if not nx.is_connected(self.G):
            raise ValueError("Warehouse graph is not connected — check edge definitions")

    def shortest_path(self, source, target):
        return nx.shortest_path(self.G, source, target, weight="travel_time")

    def path_length(self, source, target):
        return nx.shortest_path_length(self.G, source, target, weight="travel_time")

    def edge_weight(self, u, v):
        return self.G[u][v]["travel_time"]

    def nodes(self):
        return list(self.G.nodes())
