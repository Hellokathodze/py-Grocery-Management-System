class SalesController:

    def __init__(self, sales_service, inventory_controller):
        self.sales_service = sales_service
        self.inventory_controller = inventory_controller


    # ---------------- RECORD SALE (GUI VERSION) ----------------
    def record_sale(self, product_id, quantity):

        # 🔥 check stock first
        products = self.inventory_controller.get_all_products()

        for p in products:
            if p.get("product_id") == product_id:

                if p.get("stock_quantity", 0) >= quantity:

                    # ✅ reduce stock
                    p["stock_quantity"] -= quantity

                    # ✅ create sale object
                    sale = {
                        "product_id": product_id,
                        "product_name": p.get("product_name"),
                        "quantity": quantity,
                        "price_per_unit": p.get("price"),
                        "total_price": quantity * p.get("price")
                    }

                    # save sale
                    self.sales_service.record_sale(sale)

                    return True

                else:
                    return False

        return False


    # ---------------- GET ALL SALES ----------------
    def get_sales(self):
        return self.sales_service.get_sales()


    # ---------------- SALES ANALYTICS ----------------
    def get_sales_analytics(self):

        sales = self.sales_service.get_sales()

        total_revenue = sum(s.get("total_price", 0) for s in sales)

        return {
            "total_transactions": len(sales),
            "total_revenue": total_revenue
        }