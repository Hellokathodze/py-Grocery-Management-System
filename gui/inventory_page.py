from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem
)


class InventoryPage(QWidget):

    def __init__(self, inventory_controller):
        super().__init__()
        self.inventory_controller = inventory_controller
        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()

        title = QLabel("📦 Inventory")
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        btn = QPushButton("🔄 Load Products")
        btn.clicked.connect(self.load_products)
        layout.addWidget(btn)

        self.setLayout(layout)

    def load_products(self):

        products = self.inventory_controller.get_all_products()

        self.table.setRowCount(len(products))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Name", "Price", "Stock"]
        )

        for row, p in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(p.get("product_id")))
            self.table.setItem(row, 1, QTableWidgetItem(p.get("product_name")))
            self.table.setItem(row, 2, QTableWidgetItem(str(p.get("price"))))
            self.table.setItem(row, 3, QTableWidgetItem(str(p.get("stock_quantity"))))