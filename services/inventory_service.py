from datetime import datetime, timedelta


class InventoryService:

    def __init__(self, db):
        self.db = db
        self.products = db["products"]

    # ---------------- ADD PRODUCT ----------------
    def add_product(self, product_data):

        required_fields = [
            "product_id", "product_name",
            "category", "price", "stock_quantity"
        ]

        for field in required_fields:
            if field not in product_data:
                return False

        product_data["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        existing = self.products.find_one({"product_id": product_data["product_id"]})
        if existing:
            return False

        self.products.insert_one(product_data)
        return True

    # ---------------- GET ALL PRODUCTS ----------------
    def get_all_products(self):
        return list(self.products.find({}, {"_id": 0}))

    # alias
    def get_products(self):
        return self.get_all_products()

    # ---------------- GET SINGLE PRODUCT ----------------
    def get_product(self, product_id):
        return self.products.find_one(
            {"product_id": product_id},
            {"_id": 0}
        )

    # ---------------- UPDATE PRODUCT ----------------
    def update_product(self, product_id, updated_data):

        result = self.products.update_one(
            {"product_id": product_id},
            {"$set": updated_data}
        )

        return result.modified_count > 0

    # ---------------- DELETE PRODUCT ----------------
    def delete_product(self, product_id):

        result = self.products.delete_one({"product_id": product_id})
        return result.deleted_count > 0

    # ---------------- SEARCH PRODUCT ----------------
    def search_product(self, keyword):

        return list(self.products.find(
            {
                "$or": [
                    {"product_id": {"$regex": keyword, "$options": "i"}},
                    {"product_name": {"$regex": keyword, "$options": "i"}},
                    {"category": {"$regex": keyword, "$options": "i"}}
                ]
            },
            {"_id": 0}
        ))

    # ---------------- LOW STOCK ----------------
    def get_low_stock_products(self):

        return list(self.products.find(
            {
                "$expr": {
                    "$lte": ["$stock_quantity", "$reorder_level"]
                }
            },
            {"_id": 0}
        ))

    # ---------------- EXPIRY: GET ALL WITH EXPIRY INFO ----------------
    def get_products_with_expiry_status(self, warning_days=7):
        """
        Returns all products that have an expiry_date, with an
        extra 'expiry_status' field: 'expired', 'expiring_soon', or 'ok'.
        """

        products = self.get_all_products()
        today = datetime.now().date()
        warning_threshold = today + timedelta(days=warning_days)

        result = []

        for p in products:
            expiry_str = p.get("expiry_date", "")

            if not expiry_str:
                p["expiry_status"] = "no_date"
                result.append(p)
                continue

            try:
                expiry_date = datetime.strptime(str(expiry_str)[:10], "%Y-%m-%d").date()
            except (ValueError, TypeError):
                p["expiry_status"] = "no_date"
                result.append(p)
                continue

            if expiry_date < today:
                p["expiry_status"] = "expired"
                p["days_remaining"] = (expiry_date - today).days
            elif expiry_date <= warning_threshold:
                p["expiry_status"] = "expiring_soon"
                p["days_remaining"] = (expiry_date - today).days
            else:
                p["expiry_status"] = "ok"
                p["days_remaining"] = (expiry_date - today).days

            result.append(p)

        return result

    # ---------------- EXPIRY: ONLY EXPIRED ----------------
    def get_expired_products(self):

        products = self.get_products_with_expiry_status()
        return [p for p in products if p.get("expiry_status") == "expired"]

    # ---------------- EXPIRY: EXPIRING SOON ----------------
    def get_expiring_soon_products(self, warning_days=7):

        products = self.get_products_with_expiry_status(warning_days)
        return [
            p for p in products
            if p.get("expiry_status") in ("expired", "expiring_soon")
        ]

    # ---------------- INCREASE STOCK ----------------
    def increase_stock(self, product_id, quantity):

        if quantity <= 0:
            return False

        result = self.products.update_one(
            {"product_id": product_id},
            {"$inc": {"stock_quantity": quantity}}
        )

        return result.modified_count > 0

    # ---------------- DECREASE STOCK ----------------
    def decrease_stock(self, product_id, quantity):

        if quantity <= 0:
            return False

        product = self.get_product(product_id)

        if not product:
            return False

        if product.get("stock_quantity", 0) < quantity:
            return False

        result = self.products.update_one(
            {"product_id": product_id},
            {"$inc": {"stock_quantity": -quantity}}
        )

        return result.modified_count > 0

    # ---------------- INVENTORY ANALYTICS ----------------
    def get_inventory_summary(self):

        products = self.get_all_products()

        total_products = len(products)
        total_stock = sum(p.get("stock_quantity", 0) for p in products)

        return {
            "total_products": total_products,
            "total_stock": total_stock
        }