class Order:
    def __init__(self, order_id, arrival_time):
        self.order_id = order_id
        self.arrival_time = arrival_time
        self.status = "Queued"

    def update_status(self, new_status):
        self.status = new_status