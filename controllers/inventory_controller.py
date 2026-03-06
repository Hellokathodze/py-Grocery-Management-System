class InventoryController:

    def __init__(self, inventory_service):
        self.inventory_service = inventory_service

    def add_product(self):

        product_id = input("Product ID: ")
        name = input("Product Name: ")
        category = input("Category: ")
        price = float(input("Price: "))
        stock = int(input("Stock: "))

        product = {
            "product_id": product_id,
            "product_name": name,
            "category": category,
            "price": price,
            "stock": stock
        }

        self.inventory_service.add_product(product)
        print("Product added successfully!")

    def view_products(self):

        products = self.inventory_service.get_products()

        for p in products:
            print(p)

    def update_product(self):

        product_id = input("Product ID to update: ")
        price = float(input("New price: "))
        stock = int(input("New stock: "))

        self.inventory_service.update_product(product_id, {
            "price": price,
            "stock": stock
        })

        print("Product updated.")

    def delete_product(self):

        product_id = input("Product ID to delete: ")
        self.inventory_service.delete_product(product_id)
        print("Product deleted.")

    def get_products(self):
        return self.inventory_service.get_products()