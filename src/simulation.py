import random
from order import Order
from agent import Agent
from inventory import InventoryBin
from packing import PackingStation
from metrics import Metrics
from graph import WarehouseGraph


class Simulation:
    def __init__(self, arrival_rate, service_min=1, service_max=3):
        self.arrival_rate = arrival_rate
        self.service_min = service_min
        self.service_max = service_max

        self.current_time = 0
        self.worker_free_time = 0

        self.agent = Agent(1)
        self.inventory = InventoryBin(stock=20, reorder_point=5, reorder_qty=10)
        self.packing = PackingStation()
        self.metrics = Metrics()

        self.graph = self.build_warehouse_graph()
        

    def build_warehouse_graph(self):
        graph = WarehouseGraph()
        graph.add_edge("Dock", "Aisle_A", 2)
        graph.add_edge("Dock", "Aisle_B", 4)
        graph.add_edge("Aisle_A", "Aisle_C", 3)
        graph.add_edge("Aisle_B", "Aisle_C", 1)
        graph.add_edge("Aisle_C", "Packing", 2)
        graph.add_edge("Aisle_A", "Packing", 5)
        return graph

    def generate_interarrival(self):
        return random.expovariate(self.arrival_rate)

    def generate_service_time(self):
        return random.uniform(self.service_min, self.service_max)

    def generate_pickup_location(self):
        return random.choice(["Aisle_A", "Aisle_B", "Aisle_C"])

    def run(self, num_orders):
        print(f"\nArrival Rate (λ): {self.arrival_rate}")
        print(f"Simulating {num_orders} orders...\n")

        for order_id in range(1, num_orders + 1):
            interarrival = self.generate_interarrival()
            self.current_time += interarrival

            pickup_location = self.generate_pickup_location()
            order = Order(order_id, self.current_time, pickup_location)

            start_service = max(self.current_time, self.worker_free_time)
            waiting_time = start_service - self.current_time

            self.agent.pick_order(order)

            travel_to_pick, pick_path = self.agent.travel_to(order.pickup_location, self.graph)
            self.inventory.remove_stock(1)

            service_time = self.generate_service_time()

            self.agent.deliver_to_packing(order)
            travel_to_pack, pack_path = self.agent.travel_to(order.packing_location, self.graph)

            self.packing.add_to_queue(order)
            shipped_order = self.packing.process_next()

            total_service_time = service_time + travel_to_pick + travel_to_pack
            finish_time = start_service + total_service_time
            self.worker_free_time = finish_time

            self.metrics.record_order(waiting_time, total_service_time, finish_time)

            print(f"Order {order_id}")
            print(f"  Arrival Time: {self.current_time:.2f}")
            print(f"  Pickup Location: {pickup_location}")
            print(f"  Start Time: {start_service:.2f}")
            print(f"  Travel to Pick: {travel_to_pick:.2f}")
            print(f"  Travel to Pack: {travel_to_pack:.2f}")
            print(f"  Processing Time: {service_time:.2f}")
            print(f"  Finish Time: {finish_time:.2f}")
            print(f"  Waiting Time: {waiting_time:.2f}")
            print("-" * 40)

        self.metrics.summary()