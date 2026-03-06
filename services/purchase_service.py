class PurchaseService:

    def __init__(self, db):
        self.db = db
        self.collection = db["purchases"]

    def record_purchase(self, purchase):
        self.collection.insert_one(purchase)

    def get_purchases(self):
        return list(self.collection.find({}, {"_id": 0}))