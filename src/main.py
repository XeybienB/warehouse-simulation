from Simulation import Simulation


if __name__ == "__main__":
    print("=================================")
    print("Starting Warehouse Simulation...")
    print("=================================\n")

    sim = Simulation(arrival_rate=0.5)
    sim.run(num_orders=5)