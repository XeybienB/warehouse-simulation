import csv
import os
import time
from simulation import Simulation

RUNS = [
    {"run_id": "001", "purpose": "Baseline", "arrival_rate": 0.5, "num_orders": 10, "service_min": 1, "service_max": 3},
    {"run_id": "002", "purpose": "Higher Arrival Rate", "arrival_rate": 1.0, "num_orders": 10, "service_min": 1, "service_max": 3},
    {"run_id": "003", "purpose": "High Arrival Rate", "arrival_rate": 1.5, "num_orders": 10, "service_min": 1, "service_max": 3},
    {"run_id": "004", "purpose": "More Orders", "arrival_rate": 0.5, "num_orders": 15, "service_min": 1, "service_max": 3},
    {"run_id": "005", "purpose": "Balanced Load", "arrival_rate": 1.0, "num_orders": 15, "service_min": 1, "service_max": 3},
    {"run_id": "006", "purpose": "Heavy Load", "arrival_rate": 1.5, "num_orders": 15, "service_min": 1, "service_max": 3},
    {"run_id": "007", "purpose": "Faster Service", "arrival_rate": 0.5, "num_orders": 20, "service_min": 1, "service_max": 2},
    {"run_id": "008", "purpose": "Medium Load Fast Service", "arrival_rate": 1.0, "num_orders": 20, "service_min": 1, "service_max": 2},
    {"run_id": "009", "purpose": "Slower Service", "arrival_rate": 1.5, "num_orders": 20, "service_min": 2, "service_max": 4},
    {"run_id": "010", "purpose": "Stress Test", "arrival_rate": 2.0, "num_orders": 25, "service_min": 2, "service_max": 4},
]


def save_master_summary(results, filename="results/all_runs_summary.csv"):
    os.makedirs("results", exist_ok=True)

    with open(filename, "w", newline="") as csvfile:
        fieldnames = [
            "run_id",
            "purpose",
            "arrival_rate",
            "num_orders",
            "service_min",
            "service_max",
            "total_orders",
            "avg_waiting_time",
            "avg_service_time",
            "total_completion_time",
            "duration_seconds",
            "status",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    print("=================================")
    print("Running M3 Simulation Runs")
    print("=================================\n")

    all_results = []

    for config in RUNS:
        print(f"\n=== RUN {config['run_id']} : {config['purpose']} ===")

        start_time = time.time()

        sim = Simulation(
            arrival_rate=config["arrival_rate"],
            service_min=config["service_min"],
            service_max=config["service_max"],
        )
        sim.run(num_orders=config["num_orders"])

        duration = round(time.time() - start_time, 3)
        summary = sim.metrics.get_summary()

        result_row = {
            "run_id": config["run_id"],
            "purpose": config["purpose"],
            "arrival_rate": config["arrival_rate"],
            "num_orders": config["num_orders"],
            "service_min": config["service_min"],
            "service_max": config["service_max"],
            "total_orders": summary["total_orders"],
            "avg_waiting_time": summary["avg_waiting_time"],
            "avg_service_time": summary["avg_service_time"],
            "total_completion_time": summary["total_completion_time"],
            "duration_seconds": duration,
            "status": "Complete",
        }

        all_results.append(result_row)

    save_master_summary(all_results)

    print("\nAll 10 runs completed.")
    print("Results saved to results/all_runs_summary.csv")