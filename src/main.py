from Simulation import Simulation
from inventory import InventoryBin
from metrics import Metrics

if __name__ == "__main__":
    print("Starting Warehouse Simulation...")

    sim = Simulation(arrival_rate=0.5)
    sim.run(num_orders=5)

    inventory = InventoryBin(stock=20, reorder_point=5, reorder_qty=15)
    inventory.remove_stock(10)
    inventory.remove_stock(8)

    metrics = Metrics()
    metrics.record_order()
    metrics.summary()# Warehouse Simulation Project
# Entry point for the simulation
