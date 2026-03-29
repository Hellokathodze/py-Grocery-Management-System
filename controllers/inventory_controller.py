class InventoryController:

    def __init__(self, inventory_service):
        self.inventory_service = inventory_service


    # ---------------- GUI SUPPORT METHOD ----------------
    # Needed so GUI can directly fetch products
    def get_all_products(self):
        return self.inventory_service.get_all_products()


    # ---------------- ADD PRODUCT ----------------
    def add_product(self):

        product = {
            "product_id": input("Enter Product ID: "),
            "product_name": input("Enter Product Name: "),
            "category": input("Enter Category: "),
            "price": float(input("Enter Price: ")),
            "stock_quantity": int(input("Enter Stock Quantity: ")),
            "reorder_level": int(input("Enter Reorder Level: ")),
            "expiry_date": input("Enter Expiry Date (YYYY-MM-DD): ")
        }

        self.inventory_service.add_product(product)

        print("Product added successfully.")


    # ---------------- VIEW PRODUCTS ----------------
    def view_products(self):

        products = self.inventory_service.get_all_products()

        print("\n===== PRODUCT LIST =====")

        if not products:
            print("No products found.")
            return

        for p in products:

            print(f"""
Product ID      : {p.get('product_id')}
Product Name    : {p.get('product_name')}
Category        : {p.get('category')}
Price           : {p.get('price')}
Stock Quantity  : {p.get('stock_quantity')}
Reorder Level   : {p.get('reorder_level')}
Expiry Date     : {p.get('expiry_date')}
--------------------------------
""")


    # ---------------- UPDATE PRODUCT ----------------
    def update_product(self):

        product_id = input("Enter Product ID: ")

        updated_data = {
            "product_name": input("New Name: "),
            "price": float(input("New Price: ")),
            "stock_quantity": int(input("New Stock: "))
        }

        self.inventory_service.update_product(product_id, updated_data)

        print("Product updated successfully.")


    # ---------------- DELETE PRODUCT ----------------
    def delete_product(self):

        product_id = input("Enter Product ID: ")

        self.inventory_service.delete_product(product_id)

        print("Product deleted successfully.")


    # ---------------- SEARCH PRODUCT ----------------
    def search_product(self):

        keyword = input("Enter product name/id/category: ")

        products = self.inventory_service.search_product(keyword)

        print("\n======= SEARCH RESULTS =======")

        if not products:
            print("No matching products found.")
            return

        for p in products:

            print(f"""
Product ID      : {p.get('product_id')}
Product Name    : {p.get('product_name')}
Category        : {p.get('category')}
Price           : {p.get('price')}
Stock Quantity  : {p.get('stock_quantity')}
--------------------------------
""")


    # ---------------- LOW STOCK ALERT ----------------
    def low_stock_alerts(self):

        products = self.inventory_service.get_low_stock_products()

        print("\n===== LOW STOCK PRODUCTS =====")

        if not products:
            print("No low stock products.")
            return

        for p in products:

            print(f"""
Product ID      : {p.get('product_id')}
Product Name    : {p.get('product_name')}
Stock Quantity  : {p.get('stock_quantity')}
Reorder Level   : {p.get('reorder_level')}
--------------------------------
""")


    # ---------------- EXPIRY ALERTS ----------------
    def expiry_alerts(self):

        products = self.inventory_service.get_all_products()

        print("\n===== EXPIRY ALERTS =====")

        for p in products:

            expiry = p.get("expiry_date")

            if expiry:
                print(f"""
Product ID      : {p.get('product_id')}
Product Name    : {p.get('product_name')}
Expiry Date     : {expiry}
--------------------------------
""")


    # ---------------- INVENTORY ANALYTICS ----------------
    def inventory_analytics(self):

        products = self.inventory_service.get_all_products()

        total_products = len(products)
        total_stock = 0

        for p in products:
            total_stock += p.get("stock_quantity", 0)

        print("\n===== INVENTORY ANALYTICS =====")
        print("Total Products :", total_products)
        print("Total Stock    :", total_stock)


    # ---------------- REORDER SUGGESTIONS ----------------
    def reorder_suggestions(self):

        products = self.inventory_service.get_low_stock_products()

        print("\n===== REORDER SUGGESTIONS =====")

        if not products:
            print("No products need reordering.")
            return

        for p in products:

            print(f"""
Product ID      : {p.get('product_id')}
Product Name    : {p.get('product_name')}
Current Stock   : {p.get('stock_quantity')}
Reorder Level   : {p.get('reorder_level')}
--------------------------------
""")


    # ---------------- CATEGORY ANALYTICS ----------------
    def category_analytics(self):

        products = self.inventory_service.get_all_products()

        category_count = {}

        for p in products:

            category = p.get("category")

            if category not in category_count:
                category_count[category] = 0

            category_count[category] += 1

        print("\n===== CATEGORY ANALYTICS =====")

        for cat, count in category_count.items():
            print(cat, ":", count)