from datetime import datetime


class PurchaseService:

    def __init__(self, db):
        self.db = db
        self.purchases = db["purchases"]
        self.products = db["products"]
        self.stock_movements = db["stock_movements"]

    # ---------------- RECORD PURCHASE ----------------
    def record_purchase(self, product_id, quantity, cost_price):

        # 🔥 VALIDATION
        if quantity <= 0 or cost_price <= 0:
            return False

        product = self.products.find_one({"product_id": product_id})

        if not product:
            return False

        product_name = product.get("product_name")

        total_cost = quantity * cost_price

        now = datetime.now()

        purchase_data = {
            "product_id": product_id,
            "product_name": product_name,
            "quantity": quantity,
            "cost_price": cost_price,
            "total_cost": total_cost,
            "purchase_date": now.strftime("%Y-%m-%d %H:%M:%S")
        }

        # 🔥 SAVE PURCHASE
        self.purchases.insert_one(purchase_data)

        # 🔥 UPDATE STOCK (CLEAN WAY)
        self.products.update_one(
            {"product_id": product_id},
            {"$inc": {"stock_quantity": quantity}}
        )

        # 🔥 RECORD STOCK MOVEMENT
        movement = {
            "product_id": product_id,
            "product_name": product_name,
            "movement_type": "PURCHASE",
            "quantity_change": quantity,
            "reference_id": "PURCHASE_TRANSACTION",
            "date": now.strftime("%Y-%m-%d %H:%M:%S")
        }

        self.stock_movements.insert_one(movement)

        return True

    # ---------------- GET ALL PURCHASES ----------------
    def get_all_purchases(self):
        return list(self.purchases.find({}, {"_id": 0}))