class Agent:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.available = True
        self.current_location = "Dock"

    def travel_to(self, destination, graph):
        travel_time, path = graph.dijkstra(self.current_location, destination)

        print(f"Agent {self.agent_id} traveling from {self.current_location} to {destination}")
        print(f"  Path: {' -> '.join(path)}")
        print(f"  Travel Time: {travel_time}")

        self.current_location = destination
        return travel_time, path

    def pick_order(self, order):
        print(f"Agent {self.agent_id} picking Order {order.order_id}")
        order.update_status("Picking")

    def deliver_to_packing(self, order):
        print(f"Agent {self.agent_id} delivering Order {order.order_id} to packing")
        order.update_status("Ready for Packing")