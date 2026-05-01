class PackingStation:
    def __init__(self, station_id=1, service_rate=1.0):
        self.station_id = station_id
        self.service_rate = service_rate
        self.queue = []
        self.busy = False

    def add_to_queue(self, order):
        self.queue.append(order)

    def process_next(self):
        if self.queue and not self.busy:
            self.busy = True
            order = self.queue.pop(0)
            order.update_status("Packing")
            return order
        return None

    def complete_order(self, order):
        self.busy = False
        order.update_status("Shipped")
        return order
