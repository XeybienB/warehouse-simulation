import simpy
import random

from graph import WarehouseLayout
from inventory import InventoryBin
from packing import PackingStation
from metrics import MetricsCollector
from order import Order


class Dispatcher:
    """Encapsulates worker assignment policy for the simulation."""

    def __init__(self, worker_pool):
        self._pool = worker_pool

    def request_worker(self):
        return self._pool.request()

    def release_worker(self, req):
        self._pool.release(req)

    @property
    def queue_length(self):
        return len(self._pool.queue)

    @property
    def active_count(self):
        return self._pool.count


class WarehouseSimulation:
    """Top-level controller.  Maintains the SimPy environment, event queue,
    agent pool, packing station, warehouse layout, and metrics collector."""

    PICK_LOCATIONS = ["Aisle_A", "Aisle_B", "Aisle_C"]

    def __init__(self, arrival_rate, num_orders, service_min, service_max, num_workers=1):
        self.arrival_rate = arrival_rate
        self.num_orders = num_orders
        self.service_min = service_min
        self.service_max = service_max
        self.num_workers = num_workers

        self.env = simpy.Environment()

        # SimPy resources
        self._worker_resource = simpy.Resource(self.env, capacity=num_workers)
        self._packing_resource = simpy.Resource(self.env, capacity=1)

        self.layout = WarehouseLayout()
        self.dispatcher = Dispatcher(self._worker_resource)

        # One InventoryBin per pick location with (s, Q) policy
        self.inventory = {
            loc: InventoryBin(f"SKU-{loc[-1]}", loc, stock=50, reorder_point=5, reorder_qty=20)
            for loc in self.PICK_LOCATIONS
        }

        self.packing = PackingStation()
        self.metrics = MetricsCollector()

    # ------------------------------------------------------------------
    # SimPy processes
    # ------------------------------------------------------------------

    def _order_generator(self):
        for order_id in range(1, self.num_orders + 1):
            interarrival = random.expovariate(self.arrival_rate)
            yield self.env.timeout(interarrival)

            pick_loc = random.choice(self.PICK_LOCATIONS)
            order = Order(order_id, self.env.now, pick_loc)
            self.metrics.record_queue_length(self.env.now, self.dispatcher.queue_length)
            self.env.process(self._process_order(order))

    def _restock_process(self, location):
        lead_time = self.inventory[location].restock_lead_time()
        yield self.env.timeout(lead_time)
        self.inventory[location].restock()

    def _process_order(self, order):
        arrival = order.arrival_time

        # --- Phase 1: acquire a worker ---
        worker_req = self.dispatcher.request_worker()
        yield worker_req

        # Congestion factor: travel time inflated proportionally to queue depth.
        # Coefficient kept small so it models realistic aisle slowdowns, not
        # exponential blowup.
        congestion = 1.0 + 0.01 * self.dispatcher.queue_length

        # --- Phase 2: travel Dock → pick location (step-by-step via Dijkstra) ---
        path_to_pick = self.layout.shortest_path("Dock", order.pickup_location)
        for i in range(len(path_to_pick) - 1):
            weight = self.layout.edge_weight(path_to_pick[i], path_to_pick[i + 1])
            yield self.env.timeout(weight * congestion)

        # --- Phase 3: pick item and trigger restock if needed ---
        bin_ = self.inventory[order.pickup_location]
        bin_.remove(1)
        if bin_.needs_restock():
            self.env.process(self._restock_process(order.pickup_location))
        order.update_status("Picking")

        # --- Phase 4: travel pick location → packing station (step-by-step) ---
        path_to_pack = self.layout.shortest_path(order.pickup_location, "Packing")
        for i in range(len(path_to_pack) - 1):
            weight = self.layout.edge_weight(path_to_pack[i], path_to_pack[i + 1])
            yield self.env.timeout(weight * congestion)

        order.update_status("Ready for Packing")
        self.dispatcher.release_worker(worker_req)  # worker free after delivery

        # --- Phase 5: wait for packing station, then pack ---
        pack_req = self._packing_resource.request()
        yield pack_req

        packing_start = self.env.now
        service_time = random.uniform(self.service_min, self.service_max)
        yield self.env.timeout(service_time)

        self._packing_resource.release(pack_req)
        finish_time = self.env.now
        order.update_status("Shipped")

        # waiting_time = time from arrival until packing begins
        # (includes queue wait + travel + pick + packing-queue wait)
        self.metrics.record_order(arrival, packing_start, service_time, finish_time)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def run(self):
        self.env.process(self._order_generator())
        self.env.run()
        return self.metrics.get_summary()
