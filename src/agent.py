class Agent:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.available = True

    def pick_order(self, order):
        print(f"Agent {self.agent_id} picking Order {order.order_id}")
        order.update_status("Picking")

    def deliver_to_packing(self, order):
        print(f"Agent {self.agent_id} delivering Order {order.order_id} to packing")
        order.update_status("Ready for Packing")