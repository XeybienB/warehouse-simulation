import csv
import os
import sys
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
from simulation import WarehouseSimulation

RUNS = [
    # --- Single-worker runs (M3-style, extended to larger order counts) ---
    {"run_id": "001", "purpose": "Baseline",        "arrival_rate": 0.5, "num_orders":  50, "service_min": 1, "service_max": 3, "num_workers": 1},
    {"run_id": "002", "purpose": "Higher AR",        "arrival_rate": 1.0, "num_orders":  50, "service_min": 1, "service_max": 3, "num_workers": 1},
    {"run_id": "003", "purpose": "High AR",          "arrival_rate": 1.5, "num_orders":  50, "service_min": 1, "service_max": 3, "num_workers": 1},
    {"run_id": "004", "purpose": "More Orders",      "arrival_rate": 0.5, "num_orders": 100, "service_min": 1, "service_max": 3, "num_workers": 1},
    {"run_id": "005", "purpose": "Balanced",         "arrival_rate": 1.0, "num_orders": 100, "service_min": 1, "service_max": 3, "num_workers": 1},
    {"run_id": "006", "purpose": "Heavy Load",       "arrival_rate": 1.5, "num_orders": 100, "service_min": 1, "service_max": 3, "num_workers": 1},
    {"run_id": "007", "purpose": "Fast Svc",         "arrival_rate": 0.5, "num_orders": 100, "service_min": 0, "service_max": 1, "num_workers": 1},
    {"run_id": "008", "purpose": "Med Fast Svc",     "arrival_rate": 1.0, "num_orders": 100, "service_min": 0, "service_max": 1, "num_workers": 1},
    {"run_id": "009", "purpose": "Slow Svc",         "arrival_rate": 1.5, "num_orders": 100, "service_min": 2, "service_max": 4, "num_workers": 1},
    {"run_id": "010", "purpose": "Stress Test",      "arrival_rate": 2.0, "num_orders": 150, "service_min": 2, "service_max": 4, "num_workers": 1},
    # --- Multi-worker runs ---
    {"run_id": "011", "purpose": "2-Worker Baseline","arrival_rate": 0.5, "num_orders": 100, "service_min": 1, "service_max": 3, "num_workers": 2},
    {"run_id": "012", "purpose": "2-Worker Heavy",   "arrival_rate": 1.5, "num_orders": 100, "service_min": 1, "service_max": 3, "num_workers": 2},
    {"run_id": "013", "purpose": "3-Worker",         "arrival_rate": 0.5, "num_orders": 100, "service_min": 1, "service_max": 3, "num_workers": 3},
]


def save_results(results):
    out_dir = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(out_dir, exist_ok=True)
    fieldnames = [
        "run_id", "purpose", "arrival_rate", "num_orders",
        "service_min", "service_max", "num_workers",
        "avg_waiting_time", "avg_service_time", "avg_completion_time",
        "throughput", "status",
    ]
    with open(os.path.join(out_dir, "all_runs_summary.csv"), "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def generate_plots(results, run10_metrics):
    out_dir = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(out_dir, exist_ok=True)

    # Figure 1 — Queue length over time for Run 010 (Stress Test)
    if run10_metrics and run10_metrics.queue_lengths:
        times, lengths = zip(*run10_metrics.queue_lengths)
        _, ax = plt.subplots(figsize=(10, 4))
        ax.plot(times, lengths, linewidth=0.8, label="Run 010")
        ax.set_title("Queue Length Over Time for Run 010")
        ax.set_xlabel("Time")
        ax.set_ylabel("Queue Length")
        ax.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, "queue_length_run010.png"), dpi=150)
        plt.close()

    # Figure 2 — Average waiting time vs arrival rate, by workers
    _, ax = plt.subplots(figsize=(8, 5))
    for workers, marker, label in [(1, "o-b", "1 worker(s)"), (2, "s-r", "2 worker(s)"), (3, "^-g", "3 worker(s)")]:
        subset = sorted(
            [r for r in results if r["num_workers"] == workers],
            key=lambda r: r["arrival_rate"],
        )
        if subset:
            ax.plot([r["arrival_rate"] for r in subset],
                    [r["avg_waiting_time"] for r in subset],
                    marker, label=label)
    ax.set_xlabel("Arrival Rate (orders/unit time)")
    ax.set_ylabel("Average Waiting Time")
    ax.set_title("Average Waiting Time vs Arrival Rate by Number of Workers")
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "avg_wait_vs_arrival_rate.png"), dpi=150)
    plt.close()

    # Figure 3 — Average waiting time vs number of orders, by workers
    _, ax = plt.subplots(figsize=(8, 5))
    for workers, marker, label in [(1, "o-b", "1 worker(s)"), (2, "s-r", "2 worker(s)"), (3, "^-g", "3 worker(s)")]:
        subset = sorted(
            [r for r in results if r["num_workers"] == workers],
            key=lambda r: r["num_orders"],
        )
        if subset:
            ax.plot([r["num_orders"] for r in subset],
                    [r["avg_waiting_time"] for r in subset],
                    marker, label=label)
    ax.set_xlabel("Number of Orders")
    ax.set_ylabel("Average Waiting Time")
    ax.set_title("Average Waiting Time vs Number of Orders by Number of Workers")
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "avg_wait_vs_orders.png"), dpi=150)
    plt.close()

    # Figure 4 — Throughput vs arrival rate, by workers
    _, ax = plt.subplots(figsize=(8, 5))
    for workers, marker, label in [(1, "o-b", "1 worker(s)"), (2, "s-r", "2 worker(s)"), (3, "^-g", "3 worker(s)")]:
        subset = sorted(
            [r for r in results if r["num_workers"] == workers],
            key=lambda r: r["arrival_rate"],
        )
        if subset:
            ax.plot([r["arrival_rate"] for r in subset],
                    [r["throughput"] for r in subset],
                    marker, label=label)
    ax.set_xlabel("Arrival Rate (orders/unit time)")
    ax.set_ylabel("Throughput (orders/time unit)")
    ax.set_title("Throughput vs Arrival Rate by Number of Workers")
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "throughput_vs_arrival_rate.png"), dpi=150)
    plt.close()


if __name__ == "__main__":
    print("=" * 55)
    print(" Warehouse Simulation — M5 Extended Runs (13 scenarios)")
    print("=" * 55)

    all_results = []
    run10_sim = None

    for config in RUNS:
        print(f"\n=== RUN {config['run_id']}: {config['purpose']} ===")
        print(f"    λ={config['arrival_rate']}  orders={config['num_orders']}  "
              f"svc=[{config['service_min']},{config['service_max']}]  "
              f"workers={config['num_workers']}")

        wall_start = time.time()
        sim = WarehouseSimulation(
            arrival_rate=config["arrival_rate"],
            num_orders=config["num_orders"],
            service_min=config["service_min"],
            service_max=config["service_max"],
            num_workers=config["num_workers"],
        )
        sim.run()
        wall_elapsed = round(time.time() - wall_start, 3)

        s = sim.metrics.get_summary()

        if config["run_id"] == "010":
            run10_sim = sim

        row = {
            "run_id": config["run_id"],
            "purpose": config["purpose"],
            "arrival_rate": config["arrival_rate"],
            "num_orders": config["num_orders"],
            "service_min": config["service_min"],
            "service_max": config["service_max"],
            "num_workers": config["num_workers"],
            "avg_waiting_time": s["avg_waiting_time"],
            "avg_service_time": s["avg_service_time"],
            "avg_completion_time": s["avg_completion_time"],
            "throughput": s["throughput"],
            "status": "Complete",
        }
        all_results.append(row)

        print(f"    Avg Wait:   {s['avg_waiting_time']:.2f}")
        print(f"    Avg Svc:    {s['avg_service_time']:.2f}")
        print(f"    Avg Compl:  {s['avg_completion_time']:.2f}")
        print(f"    Throughput: {s['throughput']:.3f} orders/time unit")
        print(f"    Wall time:  {wall_elapsed}s")

    save_results(all_results)
    generate_plots(all_results, run10_sim.metrics if run10_sim else None)

    print("\n" + "=" * 55)
    print(" All 13 runs complete.")
    print(" Results  -> results/all_runs_summary.csv  (project root)")
    print(" Plots    -> results/*.png               (project root)")
    print("=" * 55)
