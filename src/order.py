class Order:
    def __init__(self, order_id, arrival_time, pickup_location, packing_location="Packing"):
        self.order_id = order_id
        self.arrival_time = arrival_time
        self.pickup_location = pickup_location
        self.packing_location = packing_location
        self.status = "Queued"
        self.service_start_time = None

    def update_status(self, new_status):
        self.status = new_status
