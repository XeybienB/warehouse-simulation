import random


class Simulation:
    def __init__(self, arrival_rate):
        """
        arrival_rate: lambda value for Poisson arrivals
        """
        self.arrival_rate = arrival_rate
        self.current_time = 0
        self.worker_free_time = 0  # when the worker becomes available

    def generate_interarrival(self):
        """Generate exponential interarrival time"""
        return random.expovariate(self.arrival_rate)

    def generate_service_time(self):
        """Generate service time (you can adjust distribution if needed)"""
        return random.uniform(1, 3)  # service takes between 1 and 3 time units

    def run(self, num_orders):
        print(f"Arrival Rate (λ): {self.arrival_rate}")
        print(f"Simulating {num_orders} orders...\n")

        for order_id in range(1, num_orders + 1):

            # Generate next arrival
            interarrival = self.generate_interarrival()
            self.current_time += interarrival

            # Generate service time
            service_time = self.generate_service_time()

            # Determine when service actually starts
            start_service_time = max(self.current_time, self.worker_free_time)

            # Calculate finish time
            finish_time = start_service_time + service_time

            # Update worker availability
            self.worker_free_time = finish_time

            # Calculate waiting time
            waiting_time = start_service_time - self.current_time

            print(f"Order {order_id}")
            print(f"  Arrival Time: {self.current_time:.2f}")
            print(f"  Service Start: {start_service_time:.2f}")
            print(f"  Service Time: {service_time:.2f}")
            print(f"  Finish Time: {finish_time:.2f}")
            print(f"  Waiting Time: {waiting_time:.2f}")
            print("-" * 40)