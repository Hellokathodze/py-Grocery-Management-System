from datetime import datetime


class InventoryService:

    def __init__(self, db):
        self.db = db
        self.products = db["products"]


    # ---------------- ADD PRODUCT ----------------

    def add_product(self, product_data):

        product_data["created_at"] = datetime.now()

        self.products.insert_one(product_data)

        print("Product added successfully.")


    # ---------------- GET ALL PRODUCTS ----------------

    def get_all_products(self):

        return list(self.products.find({}, {"_id": 0}))


    # alias method (used by export feature)
    def get_products(self):

        return self.get_all_products()


    # ---------------- UPDATE PRODUCT ----------------

    def update_product(self, product_id, updated_data):

        result = self.products.update_one(
            {"product_id": product_id},
            {"$set": updated_data}
        )

        if result.modified_count > 0:
            print("Product updated successfully.")
        else:
            print("Product not found.")


    # ---------------- DELETE PRODUCT ----------------

    def delete_product(self, product_id):

        result = self.products.delete_one({"product_id": product_id})

        if result.deleted_count > 0:
            print("Product deleted successfully.")
        else:
            print("Product not found.")


    # ---------------- SEARCH PRODUCT ----------------
    # FIXED VERSION

    def search_product(self, keyword):

        products = list(self.products.find({
            "$or": [
                {"product_id": {"$regex": keyword, "$options": "i"}},
                {"product_name": {"$regex": keyword, "$options": "i"}},
                {"category": {"$regex": keyword, "$options": "i"}}
            ]
        }, {"_id": 0}))

        return products


    # ---------------- LOW STOCK PRODUCTS ----------------
    # FIX FOR MENU 10 & 15

    def get_low_stock_products(self):

        products = list(self.products.find({
            "$expr": {
                "$lte": ["$stock_quantity", "$reorder_level"]
            }
        }, {"_id": 0}))

        return products


    # ---------------- INCREASE STOCK ----------------
    # used in purchase

    def increase_stock(self, product_id, quantity):

        self.products.update_one(
            {"product_id": product_id},
            {"$inc": {"stock_quantity": quantity}}
        )


    # ---------------- DECREASE STOCK ----------------
    # used in sales

    def decrease_stock(self, product_id, quantity):

        self.products.update_one(
            {"product_id": product_id},
            {"$inc": {"stock_quantity": -quantity}}
        )