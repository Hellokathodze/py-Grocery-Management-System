class InventoryController:

    def __init__(self, inventory_service):
        self.inventory_service = inventory_service

    # ---------------- GET ALL PRODUCTS ----------------
    def get_all_products(self):
        return self.inventory_service.get_all_products()

    # ---------------- ADD PRODUCT ----------------
    def add_product(self, product_data):
        return self.inventory_service.add_product(product_data)

    # ---------------- UPDATE PRODUCT ----------------
    def update_product(self, product_id, updated_data):
        return self.inventory_service.update_product(product_id, updated_data)

    # ---------------- DELETE PRODUCT ----------------
    def delete_product(self, product_id):
        return self.inventory_service.delete_product(product_id)

    # ---------------- SEARCH PRODUCT ----------------
    def search_product(self, keyword):
        return self.inventory_service.search_product(keyword)

    # ---------------- LOW STOCK ----------------
    def get_low_stock_products(self):
        return self.inventory_service.get_low_stock_products()

    # ---------------- EXPIRY: ALL WITH STATUS ----------------
    def get_products_with_expiry_status(self, warning_days=7):
        return self.inventory_service.get_products_with_expiry_status(warning_days)

    # ---------------- EXPIRY: ONLY EXPIRED ----------------
    def get_expired_products(self):
        return self.inventory_service.get_expired_products()

    # ---------------- EXPIRY: EXPIRING SOON ----------------
    def get_expiring_soon_products(self, warning_days=7):
        return self.inventory_service.get_expiring_soon_products(warning_days)

    # ---------------- INVENTORY ANALYTICS ----------------
    def get_inventory_analytics(self):
        return self.inventory_service.get_inventory_summary()

    # ---------------- CATEGORY ANALYTICS ----------------
    def get_category_analytics(self):

        products = self.inventory_service.get_all_products()

        category_count = {}

        for p in products:
            category = p.get("category", "Unknown")
            category_count[category] = category_count.get(category, 0) + 1

        return category_count