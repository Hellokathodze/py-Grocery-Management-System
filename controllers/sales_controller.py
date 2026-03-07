class SalesController:

    def __init__(self, sales_service):
        self.sales_service = sales_service


    # RECORD SALE
    def record_sale(self):

        product_id = input("Product ID: ")
        quantity = int(input("Quantity: "))

        sale = {
            "product_id": product_id,
            "quantity": quantity
        }

        result = self.sales_service.record_sale(sale)

        if result:
            print("\nSale recorded successfully.\n")
        else:
            print("\nSale failed.\n")


    # VIEW SALES
    def view_sales(self):

        sales = self.sales_service.get_sales()

        print("\n===== SALES HISTORY =====\n")

        if not sales:
            print("No sales records found.")
            return

        for sale in sales:

            print("Product ID      :", sale.get("product_id"))
            print("Product Name    :", sale.get("product_name"))
            print("Quantity        :", sale.get("quantity"))
            print("Price Per Unit  :", sale.get("price_per_unit"))
            print("Total Price     :", sale.get("total_price"))
            print("Sale Date       :", sale.get("sale_date"))
            print("Day Of Week     :", sale.get("day_of_week"))
            print("Month           :", sale.get("month"))
            print("Season          :", sale.get("season"))
            print("-" * 40)


    # SALES ANALYTICS
    def sales_analytics(self):

        sales = self.sales_service.get_sales()

        total_revenue = 0

        for s in sales:
            total_revenue += s.get("total_price", 0)

        print("\n===== SALES ANALYTICS =====")

        print("Total Sales Transactions :", len(sales))
        print("Total Revenue :", total_revenue)