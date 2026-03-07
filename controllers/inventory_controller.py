class InventoryController:

    def __init__(self, inventory_service):
        self.inventory_service = inventory_service

    def add_product(self):

        product = {
            "product_id": input("Product ID: "),
            "product_name": input("Product Name: "),
            "category": input("Category: "),
            "price": float(input("Price: ")),
            "stock_quantity": int(input("Stock Quantity: "))
        }

        self.inventory_service.add_product(product)

        print("Product added successfully.")

    def view_products(self):

        products = self.inventory_service.get_products()

        for p in products:
            print(p)

    def update_product(self):

        product_id = input("Enter product ID: ")

        updated_data = {
            "product_name": input("New Name: "),
            "category": input("New Category: "),
            "price": float(input("New Price: ")),
            "stock_quantity": int(input("New Stock: "))
        }

        self.inventory_service.update_product(product_id, updated_data)

        print("Product updated.")

    def delete_product(self):

        product_id = input("Enter product ID: ")

        self.inventory_service.delete_product(product_id)

        print("Product deleted.")

    def low_stock_alerts(self):

        products = self.inventory_service.get_low_stock_products()

        print("\nLow Stock Products:\n")

        for p in products:
            print(p)

    def search_product(self):

        keyword = input("Enter product name/id/category: ")

        results = self.inventory_service.search_product(keyword)

        print("\nSearch Results:\n")

        for r in results:
            print(r)