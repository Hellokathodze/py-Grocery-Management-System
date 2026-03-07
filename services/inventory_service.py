class InventoryService:

    def __init__(self, db):
        self.products = db["products"]

    def add_product(self, product):

        self.products.insert_one(product)

    def get_products(self):

        return list(self.products.find({}, {"_id": 0}))

    def update_product(self, product_id, updated_data):

        self.products.update_one(
            {"product_id": product_id},
            {"$set": updated_data}
        )

    def delete_product(self, product_id):

        self.products.delete_one({"product_id": product_id})

    def get_low_stock_products(self, threshold=10):

        return list(
            self.products.find(
                {"stock_quantity": {"$lt": threshold}},
                {"_id": 0}
            )
        )

    def search_product(self, keyword):

        return list(
            self.products.find(
                {
                    "$or": [
                        {"product_id": keyword},
                        {"product_name": {"$regex": keyword, "$options": "i"}},
                        {"category": {"$regex": keyword, "$options": "i"}}
                    ]
                },
                {"_id": 0}
            )
        )