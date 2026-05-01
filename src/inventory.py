import random


class InventoryBin:
    def __init__(self, sku, node, stock, reorder_point, reorder_qty):
        self.sku = sku
        self.node = node
        self.stock = stock
        self.reorder_point = reorder_point
        self.reorder_qty = reorder_qty

    def remove(self, qty):
        self.stock = max(0, self.stock - qty)

    def needs_restock(self):
        return self.stock < self.reorder_point

    def restock(self, qty=None):
        self.stock += qty if qty is not None else self.reorder_qty

    def restock_lead_time(self):
        # Stochastic lead time: exponential with mean 2 time units
        return random.expovariate(0.5)
