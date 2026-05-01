Warehouse Operations Simulation
A discrete-event simulation of warehouse order fulfillment built for CS 4632 – Modeling and Simulation at Kennesaw State University.
Author: Xeybien Borel
Course: CS 4632 – Modeling and Simulation, Spring 2025
Repository: https://github.com/XeybienB/warehouse-simulation

Project Description
This simulation models the complete lifecycle of a warehouse order — from stochastic arrival through agent-based picking, inventory management, packing, and shipment. It is designed to identify bottlenecks, evaluate staffing strategies, and measure the effect of varying demand and service conditions on order fulfillment performance.
The simulation uses:

Poisson process for stochastic order arrivals
Dijkstra's shortest-path algorithm (via NetworkX) for agent routing through the warehouse graph
(s, Q) inventory control policy for automatic restocking
SimPy discrete-event simulation engine
Matplotlib for results visualization


Features

Stochastic order arrivals modeled as a Poisson process
Graph-based warehouse layout with shortest-path agent routing
Agent-based picking with congestion modeling (travel time inflation)
(s, Q) inventory control with stochastic restocking lead times
Multiple concurrent worker support (1, 2, or 3 workers)
Packing station queue with configurable service rate
Per-run metrics export to CSV
Time-series queue length and system load collection
Parameterized experimental runs for sensitivity analysis


Installation
Requirements: Python 3.8+

Clone the repository:

bash   git clone https://github.com/XeybienB/warehouse-simulation.git
   cd warehouse-simulation

Install dependencies:

bash   pip install -r requirements.txt
Dependencies include:

simpy
networkx
numpy
pandas
matplotlib


Usage
Run the simulation with default parameters:
bashpython src/main.py
Parameters
You can configure the following parameters in src/main.py or pass them when constructing the simulation:
ParameterDescriptionDefaultarrival_rateOrders per time unit (λ)0.5num_ordersTotal orders to simulate per run10service_minMinimum service time (time units)1service_maxMaximum service time (time units)3num_workersNumber of concurrent picker agents1
Example — Run with custom parameters:
pythonsim = Simulation(arrival_rate=1.0, num_orders=50, service_min=1, service_max=3, num_workers=2)
sim.run()
Example — Run all experimental scenarios:
bashpython src/main.py --all-runs
Results are saved to all_runs_summary.csv in the project root.

Output
Each run produces:

Console output showing per-order details (arrival time, service start, service duration, finish time, waiting time)
Routing paths showing agent movement through the warehouse graph (e.g., Aisle_A -> Packing)
Summary metrics including average waiting time, average service time, total completion time, and throughput
CSV export (all_runs_summary.csv) with all run configurations and metrics for analysis

Example console output:
Starting Warehouse Simulation...
Arrival Rate (λ): 0.5
Simulating 10 orders...

Order 1
  Arrival Time: 0.49
  Pickup Location: Aisle_A
  Path: Aisle_A -> Packing
  Travel Time: 5
  Start Time: 0.49
  Processing Time: 1.24
  Finish Time: 1.73
  Waiting Time: 0.00

Repository Structure
warehouse-simulation/
├── src/
│   ├── main.py          # Entry point; configures and runs experimental scenarios
│   ├── simulation.py    # Core WarehouseSimulation class and event loop
│   ├── agent.py         # Agent and RobotAgent classes with Dijkstra routing
│   ├── inventory.py     # InventoryBin class with (s, Q) restock policy
│   ├── layout.py        # WarehouseLayout graph and shortest-path methods
│   ├── dispatcher.py    # Dispatcher class for order-agent assignment
│   ├── packing.py       # PackingStation class with queue management
│   └── metrics.py       # MetricsCollector for per-run data collection
├── all_runs_summary.csv # Exported results from all experimental runs
├── requirements.txt     # Python dependencies
└── README.md

Experimental Scenarios
The simulation was evaluated across 13 parameterized runs:
RunScenarioArrival RateOrdersWorkers1Baseline0.55012Higher Arrival Rate1.05013High Arrival Rate1.55014More Orders0.510015Balanced Load1.010016Heavy Load1.510017Faster Service0.510018Medium Load Fast Service1.010019Slower Service1.5100110Stress Test2.0150111Baseline 2 Workers0.5100212Heavy Load 2 Workers1.5100213Baseline 3 Workers0.51003
Key finding: Adding workers is the most effective performance lever. At λ=0.5 with 100 orders, average waiting time drops from 409.53 (1 worker) → 161.89 (2 workers) → 74.79 (3 workers).

Key Results

Arrival rate is the dominant driver of waiting time in single-worker configurations
Worker count provides the largest reduction in waiting time (up to 81.7% with 3 vs. 1 worker)
Throughput plateaus near 0.10 orders/time unit for a single worker regardless of arrival rate, confirming service-capacity saturation
Model behavior is consistent with M/G/1 queueing theory predictions


License
This project was developed for academic purposes at Kennesaw State University.
