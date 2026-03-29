from database.db_connection import get_database
from services.inventory_service import InventoryService
from controllers.inventory_controller import InventoryController


def test_backend():

    db = get_database()

    inventory_service = InventoryService(db)

    inventory_controller = InventoryController(inventory_service)

    products = inventory_controller.get_all_products()

    print("Backend connected successfully.")
    print(products)


if __name__ == "__main__":
    test_backend()