class MetricsCollector:
    def __init__(self):
        self.orders = []
        self.queue_lengths = []  # (time, queue_length) pairs

    def record_order(self, arrival_time, packing_start, service_time, finish_time):
        waiting_time = packing_start - arrival_time
        self.orders.append({
            "arrival_time": arrival_time,
            "packing_start": packing_start,
            "service_time": service_time,
            "finish_time": finish_time,
            "waiting_time": waiting_time,
        })

    def record_queue_length(self, time, length):
        self.queue_lengths.append((time, length))

    def get_summary(self):
        if not self.orders:
            return {
                "total_orders": 0,
                "avg_waiting_time": 0,
                "avg_service_time": 0,
                "avg_completion_time": 0,
                "throughput": 0,
            }

        total = len(self.orders)
        avg_wait = sum(o["waiting_time"] for o in self.orders) / total
        avg_svc = sum(o["service_time"] for o in self.orders) / total
        avg_compl = sum(o["finish_time"] - o["arrival_time"] for o in self.orders) / total
        last_finish = max(o["finish_time"] for o in self.orders)
        throughput = total / last_finish if last_finish > 0 else 0

        return {
            "total_orders": total,
            "avg_waiting_time": round(avg_wait, 2),
            "avg_service_time": round(avg_svc, 2),
            "avg_completion_time": round(avg_compl, 2),
            "throughput": round(throughput, 3),
        }

    def summary(self):
        s = self.get_summary()
        print(f"\n--- Simulation Summary ---")
        print(f"Total Orders Processed: {s['total_orders']}")
        print(f"Average Waiting Time:   {s['avg_waiting_time']:.2f}")
        print(f"Average Service Time:   {s['avg_service_time']:.2f}")
        print(f"Average Completion Time:{s['avg_completion_time']:.2f}")
        print(f"Throughput:             {s['throughput']:.3f} orders/time unit")
