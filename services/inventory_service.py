class InventoryService:

    def __init__(self, db):
        self.db = db
        self.collection = db["products"]

    def add_product(self, product):
        self.collection.insert_one(product)

    def get_products(self):
        return list(self.collection.find({}, {"_id": 0}))

    def update_product(self, product_id, updated_data):
        self.collection.update_one(
            {"product_id": product_id},
            {"$set": updated_data}
        )

    def delete_product(self, product_id):
        self.collection.delete_one({"product_id": product_id})