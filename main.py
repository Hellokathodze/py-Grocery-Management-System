from database.db_connection import DatabaseConnection
from database.init_db import DatabaseInitializer

from services.inventory_service import InventoryService
from services.sales_service import SalesService
from services.purchase_service import PurchaseService
from services.stock_movement_service import StockMovementService

from controllers.inventory_controller import InventoryController
from controllers.sales_controller import SalesController
from controllers.purchase_controller import PurchaseController

from utils.export_utils import ExportUtils
from utils.backup_utils import BackupUtils


def main():

    print("===== Grocery Management System =====")

    # DATABASE CONNECTION
    db = DatabaseConnection().get_database()

    # INITIALIZE COLLECTIONS
    initializer = DatabaseInitializer(db)
    initializer.initialize_collections()

    # SERVICES
    inventory_service = InventoryService(db)
    sales_service = SalesService(db)
    purchase_service = PurchaseService(db)
    stock_service = StockMovementService(db)

    # CONTROLLERS
    inventory_controller = InventoryController(inventory_service)
    sales_controller = SalesController(sales_service)
    purchase_controller = PurchaseController(purchase_service)

    while True:

        print("\n===== MENU =====")

        print("1  Add Product")
        print("2  View Products")
        print("3  Update Product")
        print("4  Delete Product")

        print("5  Record Sale")
        print("6  View Sales")

        print("7  Record Purchase")
        print("8  View Purchases")

        print("9  View Stock Movements")

        print("10 Low Stock Alerts")
        print("11 Search Product")
        print("12 Expiry Alerts")

        print("13 Sales Analytics")
        print("14 Inventory Analytics")
        print("15 Reorder Suggestions")
        print("16 Category Analytics")

        print("17 Export Sales Report")
        print("18 Export Inventory Report")

        print("19 Backup Database")
        print("20 Restore Database")

        print("0 Exit")

        choice = input("Enter choice: ")

        # INVENTORY
        if choice == "1":
            inventory_controller.add_product()

        elif choice == "2":
            inventory_controller.view_products()

        elif choice == "3":
            inventory_controller.update_product()

        elif choice == "4":
            inventory_controller.delete_product()

        # SALES
        elif choice == "5":
            sales_controller.record_sale()

        elif choice == "6":
            sales_controller.view_sales()

        # PURCHASE
        elif choice == "7":
            purchase_controller.record_purchase()

        elif choice == "8":
            purchase_controller.view_purchases()

        # STOCK MOVEMENT
        elif choice == "9":
            inventory_controller.view_stock_movements()

        # ALERTS
        elif choice == "10":
            inventory_controller.low_stock_alerts()

        elif choice == "11":
            inventory_controller.search_product()

        elif choice == "12":
            inventory_controller.expiry_alerts()

        # ANALYTICS
        elif choice == "13":
            sales_controller.sales_analytics()

        elif choice == "14":
            inventory_controller.inventory_analytics()

        elif choice == "15":
            inventory_controller.reorder_suggestions()

        elif choice == "16":
            inventory_controller.category_analytics()

        # REPORTS
        elif choice == "17":
            sales = sales_controller.get_sales()
            ExportUtils.export_sales(sales)

        elif choice == "18":
            products = inventory_controller.get_products()
            ExportUtils.export_inventory(products)

        # BACKUP
        elif choice == "19":
            BackupUtils.backup_database()

        elif choice == "20":
            BackupUtils.restore_database()

        elif choice == "0":
            print("Exiting system.")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()