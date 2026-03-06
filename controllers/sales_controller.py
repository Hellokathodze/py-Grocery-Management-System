class SalesController:

    def __init__(self, sales_service):
        self.sales_service = sales_service

    def record_sale(self):

        product_id = input("Product ID: ")
        product_name = input("Product Name: ")
        quantity = int(input("Quantity: "))
        price = float(input("Price: "))

        total_price = quantity * price

        sale = {
            "product_id": product_id,
            "product_name": product_name,
            "quantity": quantity,
            "price": price,
            "total_price": total_price
        }

        self.sales_service.record_sale(sale)

        print("Sale recorded.")

    def view_sales(self):

        sales = self.sales_service.get_sales()

        for s in sales:
            print(s)

    def get_sales(self):
        return self.sales_service.get_sales()