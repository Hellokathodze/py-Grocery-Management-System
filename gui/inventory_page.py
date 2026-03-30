from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QLineEdit, QFrame
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from utils.signal_bus import signal_bus


class InventoryPage(QWidget):

    def __init__(self, inventory_controller):
        super().__init__()
        self.inventory_controller = inventory_controller

        # 🔥 CONNECT SIGNAL FIRST (IMPORTANT)
        signal_bus.inventory_updated.connect(self.load_products)

        self.init_ui()

    def init_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # 🔥 CARD
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #2c2c54;
                border-radius: 12px;
                padding: 20px;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        # 🔥 TITLE
        title = QLabel("📦 Inventory Management")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        # 🔍 SEARCH
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search product...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #3b3b5c;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        self.search_input.textChanged.connect(self.search_products)
        layout.addWidget(self.search_input)

        # 📊 TABLE
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Name", "Price", "Stock", "Status"]
        )

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #252542;
                gridline-color: #444;
                border-radius: 8px;
            }

            QHeaderView::section {
                background-color: #3b3b5c;
                padding: 5px;
                border: none;
            }

            QTableWidget::item:hover {
                background-color: #44446a;
            }
        """)

        self.table.setSortingEnabled(False)

        layout.addWidget(self.table)

        card.setLayout(layout)
        main_layout.addWidget(card)

        self.setLayout(main_layout)

        # 🔥 INITIAL LOAD
        self.load_products()

    # ---------------- LOAD ----------------
    def load_products(self):
        print("🔥 Inventory REFRESH CALLED")

        # 🔥 FORCE COMPLETE REFRESH
        self.table.setUpdatesEnabled(False)
        self.table.clearContents()
        self.table.setRowCount(0)

        self.search_products()

        self.table.setUpdatesEnabled(True)
        self.table.viewport().update()

    # ---------------- SEARCH ----------------
    def search_products(self):

        keyword = self.search_input.text().strip()

        if keyword:
            products = self.inventory_controller.search_product(keyword)
        else:
            products = self.inventory_controller.get_all_products()

        self.populate_table(products)

    # ---------------- TABLE ----------------
    def populate_table(self, products):

        self.table.setRowCount(len(products))

        for row, p in enumerate(products):

            stock = p.get("stock_quantity", 0)

            self.table.setItem(row, 0, QTableWidgetItem(p.get("product_id")))
            self.table.setItem(row, 1, QTableWidgetItem(p.get("product_name")))
            self.table.setItem(row, 2, QTableWidgetItem(str(p.get("price"))))

            stock_item = QTableWidgetItem(str(stock))

            # 🔥 STATUS
            if stock == 0:
                color = "#ff4d4d"
                status = "🔴 Out of Stock"
            elif stock <= 10:
                color = "#ffd11a"
                status = "🟡 Low Stock"
            else:
                color = "#33cc33"
                status = "🟢 In Stock"

            stock_item.setBackground(QColor(color))

            self.table.setItem(row, 3, stock_item)
            self.table.setItem(row, 4, QTableWidgetItem(status))

        self.table.resizeColumnsToContents()