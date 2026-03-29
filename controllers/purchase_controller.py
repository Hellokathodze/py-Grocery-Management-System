class PurchaseController:

    def __init__(self, purchase_service, inventory_controller):
        self.purchase_service = purchase_service
        self.inventory_controller = inventory_controller

    # ---------------- RECORD PURCHASE (GUI VERSION) ----------------
    def record_purchase(self, product_id, quantity, cost_price):

        # create purchase data
        purchase_data = {
            "product_id": product_id,
            "quantity": quantity,
            "cost_price": cost_price
        }

        # save purchase
        self.purchase_service.record_purchase(product_id, quantity, cost_price)

        # 🔥 IMPORTANT: increase stock in inventory
        products = self.inventory_controller.get_all_products()

        for p in products:
            if p.get("product_id") == product_id:
                p["stock_quantity"] += quantity
                break

        return True

    # ---------------- GET ALL PURCHASES ----------------
    def get_all_purchases(self):
        return self.purchase_service.get_all_purchases()