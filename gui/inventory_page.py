from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QLineEdit, QFrame, QHeaderView
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from utils.signal_bus import signal_bus


class InventoryPage(QWidget):

    def __init__(self, inventory_controller):
        super().__init__()
        self.inventory_controller = inventory_controller

        signal_bus.inventory_updated.connect(self.load_products)

        self.init_ui()

    def init_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # 🔥 GLOBAL THEME
        self.setStyleSheet("""
            QWidget {
                background-color: #0F172A;
                color: #E2E8F0;
                font-size: 13px;
            }
        """)

        # 🔥 CARD CONTAINER
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #1E293B;
                border-radius: 12px;
                padding: 20px;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        # 🔥 TITLE
        title = QLabel("📦 Inventory Management")
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        # 🔍 SEARCH
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search product...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #334155;
                border-radius: 8px;
                padding: 8px;
                border: 1px solid #475569;
                color: white;
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

        # ✅ FIX HEADER (NO DISTORTION)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setMinimumHeight(42)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # ✅ FIX ROW HEIGHT
        self.table.verticalHeader().setDefaultSectionSize(38)
        self.table.verticalHeader().setVisible(False)

        # ✅ CLEAN TABLE
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setMinimumHeight(300)

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1E293B;
                border-radius: 8px;
            }

            QHeaderView::section {
                background-color: #334155;
                color: #E2E8F0;
                padding: 8px;
                border: none;
                font-weight: bold;
            }

            QTableWidget::item {
                padding: 6px;
            }

            QTableWidget::item:selected {
                background-color: #3B82F6;
            }
        """)

        layout.addWidget(self.table)

        card.setLayout(layout)
        main_layout.addWidget(card)

        self.setLayout(main_layout)

        self.load_products()

    # ---------------- LOAD ----------------
    def load_products(self):
        self.table.setRowCount(0)
        self.search_products()

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
            self.table.setItem(row, 3, QTableWidgetItem(str(stock)))

            # ✅ CLEAN STATUS (NO BLOCK BACKGROUND)
            if stock == 0:
                status_text = "● Out of Stock"
                color = "#EF4444"
            elif stock <= 10:
                status_text = "● Low Stock"
                color = "#F59E0B"
            else:
                status_text = "● In Stock"
                color = "#22C55E"

            status_item = QTableWidgetItem(status_text)
            status_item.setForeground(QColor(color))

            self.table.setItem(row, 4, status_item)