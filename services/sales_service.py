from datetime import datetime


class SalesService:

    def __init__(self, db):
        self.sales = db["sales"]
        self.products = db["products"]

    def record_sale(self, product_id, quantity):

        # Fetch product
        product = self.products.find_one({"product_id": product_id})

        if not product:
            return False

        stock = product.get("stock_quantity", 0)
        price = product.get("price", 0)

        # Stock validation
        if stock < quantity:
            return False

        now = datetime.now()

        sale_record = {
            "product_id": product_id,
            "product_name": product.get("product_name"),
            "quantity": quantity,
            "price_per_unit": price,
            "total_price": quantity * price,
            "sale_date": now.strftime("%Y-%m-%d %H:%M:%S"),
            "day_of_week": now.strftime("%A"),
            "month": now.month,
            "season": self.get_season(now.month)
        }

        # Save sale
        self.sales.insert_one(sale_record)

        # Update stock
        self.products.update_one(
            {"product_id": product_id},
            {"$inc": {"stock_quantity": -quantity}}
        )

        return True

    def get_season(self, month):
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Summer"
        elif month in [6, 7, 8, 9]:
            return "Monsoon"
        else:
            return "Autumn"

    def get_sales(self):
        return list(self.sales.find({}, {"_id": 0}))