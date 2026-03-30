class SalesController:

    def __init__(self, sales_service, inventory_controller):
        self.sales_service = sales_service
        self.inventory_controller = inventory_controller

    # ---------------- RECORD SINGLE SALE ----------------
    def record_sale(self, product_id, quantity):

        products = self.inventory_controller.get_all_products()

        for p in products:
            if p.get("product_id") == product_id:

                stock = p.get("stock_quantity", 0)

                # 🔥 STOCK VALIDATION
                if stock < quantity:
                    return False

                price = p.get("price", 0)

                sale = {
                    "product_id": product_id,
                    "product_name": p.get("product_name"),
                    "quantity": quantity,
                    "price_per_unit": price,
                    "total_price": quantity * price
                }

                # 🔥 IMPORTANT: Let service handle DB + stock
                return self.sales_service.record_sale(sale)

        return False

    # ---------------- BULK SALE (BILLING) ----------------
    def record_bulk_sale(self, cart_items):

        for item in cart_items:

            success = self.record_sale(
                item.get("product_id"),
                item.get("qty")
            )

            if not success:
                return False

        return True

    # ---------------- GET SALES ----------------
    def get_sales(self):
        return self.sales_service.get_sales()

    # ---------------- ANALYTICS ----------------
    def get_sales_analytics(self):

        sales = self.sales_service.get_sales()

        total_revenue = sum(s.get("total_price", 0) for s in sales)

        return {
            "total_transactions": len(sales),
            "total_revenue": total_revenue
        }

    # ---------------- GET PRODUCTS ----------------
    def get_products(self):
        return self.inventory_controller.get_all_products()