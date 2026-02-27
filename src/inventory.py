class InventoryBin:
    def __init__(self, stock, reorder_point, reorder_qty):
        self.stock = stock
        self.reorder_point = reorder_point
        self.reorder_qty = reorder_qty

    def remove_stock(self, qty):
        self.stock -= qty
        print(f"Stock reduced. Current stock: {self.stock}")

        if self.stock <= self.reorder_point:
            self.restock()

    def restock(self):
        print("Reorder triggered!")
        self.stock += self.reorder_qty
        print(f"Stock after restock: {self.stock}")