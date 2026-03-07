from datetime import datetime


class SalesService:

    def __init__(self, db):
        self.db = db
        self.sales = db["sales"]
        self.products = db["products"]

    def record_sale(self, sale):

        product_id = sale["product_id"]
        quantity = sale["quantity"]

        # FETCH PRODUCT
        product = self.products.find_one({"product_id": product_id})

        if not product:
            print("Product not found.")
            return

        product_name = product.get("product_name")
        price = product.get("price", 0)
        stock = product.get("stock_quantity", 0)

        # CHECK STOCK
        if stock < quantity:
            print("Not enough stock available.")
            return

        total_price = quantity * price

        # CURRENT DATE
        now = datetime.now()

        day_of_week = now.strftime("%A")
        month = now.month

        # SEASON CALCULATION
        if month in [12, 1, 2]:
            season = "Winter"
        elif month in [3, 4, 5]:
            season = "Summer"
        elif month in [6, 7, 8, 9]:
            season = "Monsoon"
        else:
            season = "Autumn"

        sale_record = {
            "product_id": product_id,
            "product_name": product_name,
            "quantity": quantity,
            "price": price,
            "total_price": total_price,
            "date": now,
            "day_of_week": day_of_week,
            "month": month,
            "season": season
        }

        # INSERT SALE
        self.sales.insert_one(sale_record)

        # UPDATE STOCK
        self.products.update_one(
            {"product_id": product_id},
            {"$inc": {"stock_quantity": -quantity}}
        )

    def get_sales(self):
        return list(self.sales.find({}, {"_id": 0}))