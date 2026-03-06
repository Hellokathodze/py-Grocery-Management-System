class StockMovementService:

    def __init__(self, db):
        self.db = db
        self.collection = db["stock_movements"]

    def record_movement(self, movement):
        self.collection.insert_one(movement)

    def get_movements(self):
        return list(self.collection.find({}, {"_id": 0}))