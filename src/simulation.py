import random
import math
from order import Order

class Simulation:
    def __init__(self, arrival_rate):
        self.arrival_rate = arrival_rate
        self.current_time = 0
        self.order_count = 0

    def poisson_arrival(self):
        return -math.log(1.0 - random.random()) / self.arrival_rate

    def generate_order(self):
        self.order_count += 1
        arrival_time = self.current_time
        order = Order(self.order_count, arrival_time)
        print(f"Order {order.order_id} arrived at time {arrival_time}")
        return order

    def run(self, num_orders):
        for _ in range(num_orders):
            interarrival = self.poisson_arrival()
            self.current_time += interarrival
            self.generate_order()