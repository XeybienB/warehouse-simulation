class Metrics:
    def __init__(self):
        self.orders_processed = 0

    def record_order(self):
        self.orders_processed += 1

    def summary(self):
        print("\n--- Simulation Summary ---")
        print(f"Total Orders Processed: {self.orders_processed}")