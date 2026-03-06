class PurchaseController:

    def __init__(self, purchase_service):
        self.purchase_service = purchase_service

    def record_purchase(self):

        product_id = input("Product ID: ")
        product_name = input("Product Name: ")
        quantity = int(input("Quantity: "))
        price = float(input("Purchase price: "))

        purchase = {
            "product_id": product_id,
            "product_name": product_name,
            "quantity": quantity,
            "price": price
        }

        self.purchase_service.record_purchase(purchase)

        print("Purchase recorded.")

    def view_purchases(self):

        purchases = self.purchase_service.get_purchases()

        for p in purchases:
            print(p)