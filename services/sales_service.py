from datetime import datetime


class SalesService:

    def __init__(self, db):
        self.sales = db["sales"]
        self.products = db["products"]

    # 🔥 RECORD SINGLE SALE
    def record_sale(self, sale):

        product_id = sale.get("product_id")
        quantity = sale.get("quantity")

        product = self.products.find_one({"product_id": product_id})

        if not product:
            return False

        stock = product.get("stock_quantity", 0)

        # 🔥 STOCK VALIDATION
        if stock < quantity:
            return False

        now = datetime.now()

        sale_record = {
            "product_id": product_id,
            "product_name": sale.get("product_name"),
            "quantity": quantity,
            "price_per_unit": sale.get("price_per_unit"),
            "total_price": sale.get("total_price"),
            "sale_date": now.strftime("%Y-%m-%d %H:%M:%S"),
            "day_of_week": now.strftime("%A"),
            "month": now.month,
            "season": self.get_season(now.month)
        }

        # SAVE SALE
        self.sales.insert_one(sale_record)

        # UPDATE STOCK
        self.products.update_one(
            {"product_id": product_id},
            {"$inc": {"stock_quantity": -quantity}}
        )

        return True

    # 🔥 NEW: RECORD FULL BILL (MULTIPLE ITEMS)
    def record_bulk_sale(self, cart_items):

        for item in cart_items:

            sale = {
                "product_id": item.get("id"),
                "product_name": item.get("name"),
                "quantity": item.get("qty"),
                "price_per_unit": item.get("price"),
                "total_price": item.get("total")
            }

            success = self.record_sale(sale)

            if not success:
                return False

        return True

    # ---------------- GET SALES ----------------
    def get_sales(self):
        return list(self.sales.find({}, {"_id": 0}))

    # ---------------- ANALYTICS ----------------
    def get_sales_analytics(self):

        sales = self.get_sales()

        total_revenue = sum(s.get("total_price", 0) for s in sales)

        return {
            "total_transactions": len(sales),
            "total_revenue": total_revenue
        }

    # ---------------- SEASON ----------------
    def get_season(self, month):
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Summer"
        elif month in [6, 7, 8, 9]:
            return "Monsoon"
        else:
            return "Autumn"