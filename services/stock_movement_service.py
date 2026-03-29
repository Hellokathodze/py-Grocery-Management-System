from datetime import datetime


class StockMovementService:

    def __init__(self, db):
        self.db = db

    def record_movement(self, product_id, product_name, movement_type, quantity_change, reference_id):
        """
        Records stock movement for purchase or sale
        """

        movement_data = {
            "product_id": product_id,
            "product_name": product_name,
            "movement_type": movement_type,
            "quantity_change": quantity_change,
            "reference_id": reference_id,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.db.stock_movements.insert_one(movement_data)

    def get_all_movements(self):

        movements = list(self.db.stock_movements.find({}, {"_id": 0}))

        return movements