class StockMovementService:

    def __init__(self, db):
        self.movements = db["stock_movements"]

    def record_movement(self, product_id, movement_type, quantity):

        movement = {
            "product_id": product_id,
            "movement_type": movement_type,
            "quantity": quantity
        }

        self.movements.insert_one(movement)

    def get_movements(self):
        return list(self.movements.find({}, {"_id": 0}))