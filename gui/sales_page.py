from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox,
    QPushButton, QMessageBox, QSpinBox,
    QFrame, QTableWidget, QTableWidgetItem, QHBoxLayout
)
from PyQt6.QtCore import Qt
from utils.signal_bus import signal_bus


class SalesPage(QWidget):

    def __init__(self, sales_controller):
        super().__init__()

        self.sales_controller = sales_controller
        self.inventory_controller = sales_controller.inventory_controller

        self.cart = []
        self.products = []

        self.init_ui()

    def init_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #2c2c54;
                border-radius: 12px;
                padding: 20px;
            }
        """)

        layout = QVBoxLayout()

        title = QLabel("🛒 Cashier Billing")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        # 🔥 PRODUCT + QTY ROW
        row = QHBoxLayout()

        self.product_dropdown = QComboBox()
        row.addWidget(self.product_dropdown)

        self.quantity = QSpinBox()
        self.quantity.setMinimum(1)
        row.addWidget(self.quantity)

        layout.addLayout(row)

        # STOCK LABEL
        self.stock_label = QLabel("Stock: ")
        layout.addWidget(self.stock_label)

        # BUTTONS
        add_btn = QPushButton("➕ Add to Cart")
        add_btn.clicked.connect(self.add_to_cart)
        layout.addWidget(add_btn)

        remove_btn = QPushButton("❌ Remove Selected")
        remove_btn.clicked.connect(self.remove_item)
        layout.addWidget(remove_btn)

        # TABLE
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "Qty", "Price", "Total"])
        layout.addWidget(self.table)

        # TOTAL
        self.total_label = QLabel("Total: ₹0")
        self.total_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.total_label)

        # CHECKOUT
        checkout_btn = QPushButton("🧾 Checkout & Print Bill")
        checkout_btn.clicked.connect(self.checkout)
        layout.addWidget(checkout_btn)

        card.setLayout(layout)
        main_layout.addWidget(card)
        self.setLayout(main_layout)

        self.load_products()

    # ---------------- LOAD PRODUCTS ----------------
    def load_products(self):

        self.products = self.inventory_controller.get_all_products()
        self.product_dropdown.clear()

        for p in self.products:
            self.product_dropdown.addItem(
                f"{p['product_id']} - {p['product_name']}"
            )

        self.product_dropdown.currentIndexChanged.connect(self.update_stock)
        self.update_stock()

    # ---------------- STOCK DISPLAY ----------------
    def update_stock(self):

        index = self.product_dropdown.currentIndex()

        if index < 0 or index >= len(self.products):
            return

        product = self.products[index]
        stock = product.get("stock_quantity", 0)

        self.stock_label.setText(f"Stock: {stock}")

    # ---------------- ADD TO CART ----------------
    def add_to_cart(self):

        index = self.product_dropdown.currentIndex()

        if index < 0:
            return

        product = self.products[index]
        qty = self.quantity.value()
        stock = product.get("stock_quantity", 0)

        if qty > stock:
            QMessageBox.warning(self, "Error", "Not enough stock!")
            return

        # 🔥 HANDLE DUPLICATE ITEMS
        for item in self.cart:
            if item["product_id"] == product["product_id"]:
                item["qty"] += qty
                item["total"] = item["qty"] * item["price"]
                self.update_table()
                return

        # NEW ITEM
        self.cart.append({
            "product_id": product["product_id"],
            "name": product["product_name"],
            "qty": qty,
            "price": product["price"],
            "total": qty * product["price"]
        })

        self.update_table()

    # ---------------- REMOVE ITEM ----------------
    def remove_item(self):

        row = self.table.currentRow()

        if row >= 0:
            self.cart.pop(row)
            self.update_table()

    # ---------------- UPDATE TABLE ----------------
    def update_table(self):

        self.table.setRowCount(len(self.cart))
        total_bill = 0

        for row, item in enumerate(self.cart):

            self.table.setItem(row, 0, QTableWidgetItem(item["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(item["qty"])))
            self.table.setItem(row, 2, QTableWidgetItem(str(item["price"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(item["total"])))

            total_bill += item["total"]

        self.total_label.setText(f"Total: ₹{total_bill}")

    # ---------------- CHECKOUT ----------------
    def checkout(self):

        if not self.cart:
            QMessageBox.warning(self, "Error", "Cart is empty!")
            return

        # 🔥 USE BULK SALE
        success = self.sales_controller.record_bulk_sale(self.cart)

        if not success:
            QMessageBox.warning(self, "Error", "Sale failed due to stock issue!")
            return

        self.print_bill()

        self.cart.clear()
        self.table.setRowCount(0)
        self.total_label.setText("Total: ₹0")

        # 🔥 REFRESH STOCK
        self.load_products()
        signal_bus.inventory_updated.emit()
        QMessageBox.information(self, "Success", "Sale completed!")

    # ---------------- PRINT BILL ----------------
    def print_bill(self):

        print("\n======= BILL =======")

        total = 0

        for item in self.cart:
            print(f"{item['name']} x {item['qty']} = ₹{item['total']}")
            total += item["total"]

        print("-------------------")
        print(f"TOTAL: ₹{total}")
        print("===================")