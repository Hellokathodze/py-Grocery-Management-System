import sys
from PyQt6.QtWidgets import QApplication

from database.db_connection import DatabaseConnection
from database.init_db import DatabaseInitializer

from services.inventory_service import InventoryService
from services.sales_service import SalesService
from services.purchase_service import PurchaseService
from services.stock_movement_service import StockMovementService
from services.auth_service import AuthService

from controllers.inventory_controller import InventoryController
from controllers.sales_controller import SalesController
from controllers.purchase_controller import PurchaseController
from controllers.auth_controller import AuthController

from gui.login_window import LoginWindow


def main():

    # ---------------- DATABASE ----------------
    db_connection = DatabaseConnection()
    db = db_connection.get_database()

    initializer = DatabaseInitializer(db)
    initializer.initialize_collections()

    print("Database initialized successfully!")

    # ---------------- SERVICES ----------------
    inventory_service = InventoryService(db)
    sales_service = SalesService(db)
    purchase_service = PurchaseService(db)
    stock_service = StockMovementService(db)
    auth_service = AuthService(db)

    auth_service.create_default_users()

    # ---------------- CONTROLLERS ----------------
    inventory_controller = InventoryController(inventory_service)
    sales_controller = SalesController(sales_service, inventory_controller)
    purchase_controller = PurchaseController(purchase_service, inventory_controller)
    auth_controller = AuthController(auth_service)

    # ---------------- GUI APP ----------------
    app = QApplication(sys.argv)

    login_window = LoginWindow()

    # 🔥 inject controllers into GUI (FIXED INDENTATION)
    login_window.auth_controller = auth_controller
    login_window.inventory_controller = inventory_controller
    login_window.sales_controller = sales_controller
    login_window.purchase_controller = purchase_controller

    login_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()