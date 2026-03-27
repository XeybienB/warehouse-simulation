class Metrics:
    def __init__(self):
        self.orders_processed = 0
        self.total_waiting_time = 0
        self.total_service_time = 0
        self.total_completion_time = 0

    def record_order(self, waiting_time, service_time, finish_time):
        self.orders_processed += 1
        self.total_waiting_time += waiting_time
        self.total_service_time += service_time
        self.total_completion_time = max(self.total_completion_time, finish_time)

    def get_summary(self):
        avg_wait = self.total_waiting_time / self.orders_processed if self.orders_processed else 0
        avg_service = self.total_service_time / self.orders_processed if self.orders_processed else 0

        return {
            "total_orders": self.orders_processed,
            "avg_waiting_time": round(avg_wait, 2),
            "avg_service_time": round(avg_service, 2),
            "total_completion_time": round(self.total_completion_time, 2),
        }

    def summary(self):
        summary = self.get_summary()
        print("\n--- Simulation Summary ---")
        print(f"Total Orders Processed: {summary['total_orders']}")
        print(f"Average Waiting Time: {summary['avg_waiting_time']:.2f}")
        print(f"Average Service Time: {summary['avg_service_time']:.2f}")
        print(f"Total Completion Time: {summary['total_completion_time']:.2f}")