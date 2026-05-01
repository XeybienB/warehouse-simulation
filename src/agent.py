class Agent:
    def __init__(self, agent_id, start_location="Dock"):
        self.agent_id = agent_id
        self.current_location = start_location
        self.available = True

    def compute_route(self, layout, destination):
        return layout.shortest_path(self.current_location, destination)

    def move_step(self, destination):
        self.current_location = destination

    def pick_item(self, order, inventory_bin):
        order.update_status("Picking")
        inventory_bin.remove(1)

    def deliver_to(self, order, destination):
        self.current_location = destination
        order.update_status("Ready for Packing")


class RobotAgent(Agent):
    def __init__(self, agent_id, start_location="Dock", battery_capacity=100):
        super().__init__(agent_id, start_location)
        self.battery_level = battery_capacity
        self.battery_capacity = battery_capacity

    def consume_battery(self, amount):
        self.battery_level = max(0, self.battery_level - amount)

    def recharge(self):
        self.battery_level = self.battery_capacity
