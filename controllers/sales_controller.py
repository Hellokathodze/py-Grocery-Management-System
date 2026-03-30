class SalesController:

    def __init__(self, sales_service):
        self.sales_service = sales_service

    # ✅ RECORD SALE
    def record_sale(self, product_id, quantity):
        return self.sales_service.record_sale(product_id, quantity)

    # ✅ GET ALL SALES
    def get_sales(self):
        return self.sales_service.get_sales()

    # ✅ SALES ANALYTICS
    def get_sales_analytics(self):
        sales = self.sales_service.get_sales()

        total_revenue = sum(s.get("total_price", 0) for s in sales)

        return {
            "total_transactions": len(sales),
            "total_revenue": total_revenue
        }

    # 🔥 NEW: GET PRODUCTS (FIX FOR SALES PAGE)
    def get_products(self):
        return list(self.sales_service.products.find({}, {"_id": 0}))