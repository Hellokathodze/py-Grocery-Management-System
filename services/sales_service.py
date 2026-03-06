class SalesService:

    def __init__(self, db):
        self.db = db
        self.collection = db["sales"]

    def record_sale(self, sale):
        self.collection.insert_one(sale)

    def get_sales(self):
        return list(self.collection.find({}, {"_id": 0}))