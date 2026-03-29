class InventoryController:

    def __init__(self, inventory_service):
        self.inventory_service = inventory_service

    # ---------------- GET ALL PRODUCTS ----------------
    def get_all_products(self):
        return self.inventory_service.get_all_products()

    # ---------------- ADD PRODUCT ----------------
    def add_product(self, product_data):
        self.inventory_service.add_product(product_data)
        return True

    # ---------------- UPDATE PRODUCT ----------------
    def update_product(self, product_id, updated_data):
        self.inventory_service.update_product(product_id, updated_data)
        return True

    # ---------------- DELETE PRODUCT ----------------
    def delete_product(self, product_id):
        self.inventory_service.delete_product(product_id)
        return True

    # ---------------- SEARCH PRODUCT ----------------
    def search_product(self, keyword):
        return self.inventory_service.search_product(keyword)

    # ---------------- LOW STOCK ----------------
    def get_low_stock_products(self):
        return self.inventory_service.get_low_stock_products()

    # ---------------- EXPIRY ALERTS ----------------
    def get_expiry_products(self):
        products = self.inventory_service.get_all_products()

        expiry_list = []
        for p in products:
            if p.get("expiry_date"):
                expiry_list.append(p)

        return expiry_list

    # ---------------- ANALYTICS ----------------
    def get_inventory_analytics(self):
        products = self.inventory_service.get_all_products()

        total_products = len(products)
        total_stock = sum(p.get("stock_quantity", 0) for p in products)

        return {
            "total_products": total_products,
            "total_stock": total_stock
        }

    # ---------------- CATEGORY ANALYTICS ----------------
    def get_category_analytics(self):
        products = self.inventory_service.get_all_products()

        category_count = {}

        for p in products:
            category = p.get("category", "Unknown")
            category_count[category] = category_count.get(category, 0) + 1

        return category_count

    # ---------------- REDUCE STOCK (VERY IMPORTANT) ----------------
    def reduce_stock(self, product_name):
        products = self.inventory_service.get_all_products()

        for p in products:
            if p.get("product_name") == product_name:
                if p.get("stock_quantity", 0) > 0:
                    p["stock_quantity"] -= 1
                    return True
                return Falses