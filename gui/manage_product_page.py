from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QMessageBox
)
from utils.signal_bus import signal_bus


class ManageProductPage(QWidget):

    def __init__(self, inventory_controller):
        super().__init__()
        self.inventory_controller = inventory_controller
        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()
        layout.setSpacing(10)

        title = QLabel("🛠 Manage Products")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        # 🔥 FORM
        form_layout = QHBoxLayout()

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Product ID")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Category")

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Price")

        self.stock_input = QLineEdit()
        self.stock_input.setPlaceholderText("Stock")

        form_layout.addWidget(self.id_input)
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.category_input)
        form_layout.addWidget(self.price_input)
        form_layout.addWidget(self.stock_input)

        layout.addLayout(form_layout)

        # 🔥 BUTTONS
        btn_layout = QHBoxLayout()

        add_btn = QPushButton("Add")
        update_btn = QPushButton("Update")
        delete_btn = QPushButton("Delete")

        add_btn.clicked.connect(self.add_product)
        update_btn.clicked.connect(self.update_product)
        delete_btn.clicked.connect(self.delete_product)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(update_btn)
        btn_layout.addWidget(delete_btn)

        layout.addLayout(btn_layout)

        # 🔥 TABLE
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Name", "Category", "Price", "Stock"]
        )

        self.table.cellClicked.connect(self.fill_form)

        layout.addWidget(self.table)

        self.setLayout(layout)

        self.load_products()

    # ---------------- LOAD ----------------
    def load_products(self):

        products = self.inventory_controller.get_all_products()

        self.table.setRowCount(len(products))

        for row, p in enumerate(products):

            self.table.setItem(row, 0, QTableWidgetItem(p["product_id"]))
            self.table.setItem(row, 1, QTableWidgetItem(p["product_name"]))
            self.table.setItem(row, 2, QTableWidgetItem(p.get("category", "")))
            self.table.setItem(row, 3, QTableWidgetItem(str(p["price"])))
            self.table.setItem(row, 4, QTableWidgetItem(str(p["stock_quantity"])))

    # ---------------- FILL FORM ----------------
    def fill_form(self, row, column):

        self.id_input.setText(self.table.item(row, 0).text())
        self.name_input.setText(self.table.item(row, 1).text())
        self.category_input.setText(self.table.item(row, 2).text())
        self.price_input.setText(self.table.item(row, 3).text())
        self.stock_input.setText(self.table.item(row, 4).text())

    # ---------------- ADD ----------------
    def add_product(self):

        try:
            data = {
                "product_id": self.id_input.text(),
                "product_name": self.name_input.text(),
                "category": self.category_input.text(),
                "price": float(self.price_input.text()),
                "stock_quantity": int(self.stock_input.text())
            }

            self.inventory_controller.add_product(data)

            signal_bus.inventory_updated.emit()  # 🔥 IMPORTANT

            QMessageBox.information(self, "Success", "Product added")
            self.load_products()

        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid input!")

    # ---------------- UPDATE ----------------
    def update_product(self):

        if not self.id_input.text():
            QMessageBox.warning(self, "Error", "Select a product!")
            return

        try:
            product_id = self.id_input.text()

            updated_data = {
                "product_name": self.name_input.text(),
                "category": self.category_input.text(),
                "price": float(self.price_input.text()),
                "stock_quantity": int(self.stock_input.text())
            }

            self.inventory_controller.update_product(product_id, updated_data)

            signal_bus.inventory_updated.emit()  # 🔥 FIX ADDED

            QMessageBox.information(self, "Updated", "Product updated")
            self.load_products()

        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid input!")

    # ---------------- DELETE ----------------
    def delete_product(self):

        product_id = self.id_input.text()

        if not product_id:
            QMessageBox.warning(self, "Error", "Select a product!")
            return

        self.inventory_controller.delete_product(product_id)

        signal_bus.inventory_updated.emit()  # 🔥 FIX ADDED

        QMessageBox.information(self, "Deleted", "Product removed")
        self.load_products()