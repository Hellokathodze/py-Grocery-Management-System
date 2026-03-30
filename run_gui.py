import sys

from PyQt6.QtWidgets import QApplication, QMessageBox

from gui.login_window import LoginWindow

# Controllers
from controllers.auth_controller import AuthController
from controllers.inventory_controller import InventoryController
from controllers.sales_controller import SalesController
from controllers.purchase_controller import PurchaseController

# Services
from services.auth_service import AuthService
from services.inventory_service import InventoryService
from services.sales_service import SalesService
from services.purchase_service import PurchaseService

# Database
from database.db_connection import get_database


def main():
    try:
        app = QApplication(sys.argv)

        # 🔥 STEP 1: DB CONNECTION
        db = get_database()

        # 🔥 STEP 2: SERVICES
        auth_service = AuthService(db)
        inventory_service = InventoryService(db)
        sales_service = SalesService(db)
        purchase_service = PurchaseService(db)

        # 🔥 STEP 3: INIT DEFAULT USERS
        auth_service.create_default_users()

        # 🔥 STEP 4: CONTROLLERS

        # Inventory FIRST
        inventory_controller = InventoryController(inventory_service)

        # Auth
        auth_controller = AuthController(auth_service)

        # ✅ FIXED HERE
        sales_controller = SalesController(sales_service)

        # Purchase (keep as is if required)
        purchase_controller = PurchaseController(purchase_service, inventory_controller)

        # 🔥 STEP 5: GUI
        window = LoginWindow(
            auth_controller,
            inventory_controller,
            sales_controller,
            purchase_controller
        )
        window.show()

        sys.exit(app.exec())

    except Exception as e:
        error_box = QMessageBox()
        error_box.setWindowTitle("Application Error")
        error_box.setText("Failed to start the application.")
        error_box.setDetailedText(str(e))
        error_box.exec()


if __name__ == "__main__":
    main()