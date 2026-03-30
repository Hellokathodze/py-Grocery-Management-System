class PurchaseController:

    def __init__(self, purchase_service, inventory_controller):
        self.purchase_service = purchase_service
        self.inventory_controller = inventory_controller

    # ---------------- RECORD PURCHASE ----------------
    def record_purchase(self, product_id, quantity, cost_price):

        # 🔥 CALL SERVICE ONLY
        return self.purchase_service.record_purchase(
            product_id,
            quantity,
            cost_price
        )

    # ---------------- GET ALL PURCHASES ----------------
    def get_all_purchases(self):
        return self.purchase_service.get_all_purchases()