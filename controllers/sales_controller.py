class SalesController:

    def __init__(self, sales_service):
        self.sales_service = sales_service

    def record_sale(self):

        sale = {
            "product_id": input("Product ID: "),
            "quantity": int(input("Quantity: "))
        }

        self.sales_service.record_sale(sale)

    def view_sales(self):

        sales = self.sales_service.get_sales()

        for s in sales:
            print(s)