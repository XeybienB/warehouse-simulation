class PackingStation:
    def __init__(self):
        self.queue = []

    def add_to_queue(self, order):
        self.queue.append(order)
        print(f"Order {order.order_id} added to packing queue")

    def process_next(self):
        if self.queue:
            order = self.queue.pop(0)
            print(f"Packing Order {order.order_id}")
            order.update_status("Shipped")
            return order
        return None