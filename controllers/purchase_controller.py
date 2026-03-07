class PurchaseController:

    def __init__(self, purchase_service):
        self.purchase_service = purchase_service

    def record_purchase(self):

        product_id = input("Enter Product ID: ")
        quantity = int(input("Enter Quantity: "))
        cost_price = float(input("Enter Cost Price: "))

        self.purchase_service.record_purchase(product_id, quantity, cost_price)

    def view_purchases(self):

        purchases = self.purchase_service.get_all_purchases()

        if not purchases:
            print("No purchases found.")
            return

        print("\n===== PURCHASE HISTORY =====")

        for p in purchases:

            print(f"""
Product ID    : {p.get('product_id')}
Product Name  : {p.get('product_name')}
Quantity      : {p.get('quantity')}
Cost Price    : {p.get('cost_price')}
Total Cost    : {p.get('total_cost')}
Purchase Date : {p.get('purchase_date')}
""")