from datetime import datetime
from services.inventory_service import InventoryService
from services.stock_movement_service import StockMovementService


class PurchaseService:

    def __init__(self, db):
        self.db = db

    def record_purchase(self, product_id, quantity, cost_price):

        product = self.db.products.find_one({"product_id": product_id})

        if not product:
            print("Product not found.")
            return

        product_name = product["product_name"]

        total_cost = quantity * cost_price

        purchase_date = datetime.now()

        purchase_data = {
            "product_id": product_id,
            "product_name": product_name,
            "quantity": quantity,
            "cost_price": cost_price,
            "total_cost": total_cost,
            "purchase_date": purchase_date.strftime("%Y-%m-%d %H:%M:%S")
        }

        self.db.purchases.insert_one(purchase_data)

        # update inventory stock
        inventory_service = InventoryService(self.db)
        inventory_service.increase_stock(product_id, quantity)

        # record stock movement
        stock_service = StockMovementService(self.db)
        stock_service.record_movement(
            product_id,
            product_name,
            "PURCHASE",
            quantity,
            "PURCHASE_TRANSACTION"
        )

        print("Purchase recorded successfully.")

    def get_all_purchases(self):

        purchases = list(self.db.purchases.find({}, {"_id": 0}))

        return purchases