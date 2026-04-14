from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QLineEdit, QFrame, QHeaderView,
    QSizePolicy, QAbstractItemView
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

        # GLOBAL THEME
        self.setStyleSheet("""
            QWidget {
                background-color: #0F172A;
                color: #E2E8F0;
                font-size: 13px;
            }
        """)

        # CARD — no padding in stylesheet, use layout margins only
        card = QFrame()
        card.setObjectName("inventoryCard")
        card.setStyleSheet("""
            QFrame#inventoryCard {
                background-color: #1E293B;
                border-radius: 12px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # TITLE
        title = QLabel("📦 Inventory Management")
        title.setStyleSheet(
            "font-size: 22px; font-weight: bold; color: #F1F5F9; "
            "background: transparent; border: none;"
        )
        layout.addWidget(title)

        # SEARCH
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search product...")
        self.search_input.setMinimumHeight(40)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #0F172A;
                border-radius: 10px;
                padding: 8px 14px;
                border: 1.5px solid #2A3A55;
                color: white;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1.5px solid #3B82F6;
                background-color: #111E36;
            }
            QLineEdit:hover {
                border: 1.5px solid #3B6ECF;
            }
        """)
        self.search_input.textChanged.connect(self.search_products)
        layout.addWidget(self.search_input)

        # TABLE
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Product Name", "Price (₹)", "Stock Level", "Status"]
        )

        # Header setup
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setStretchLastSection(True)
        header.setMinimumHeight(40)
        header.setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        # Row settings
        self.table.verticalHeader().setDefaultSectionSize(40)
        self.table.verticalHeader().setVisible(False)

        # Table behavior
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.table.setMinimumHeight(300)

        self.table.setStyleSheet(self.table_style())

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
            price = p.get("price", 0)

            id_item = QTableWidgetItem(str(p.get("product_id", "")))
            name_item = QTableWidgetItem(p.get("product_name", ""))
            price_item = QTableWidgetItem(f"₹{price:,.2f}")
            stock_item = QTableWidgetItem(str(stock))

            # Center align numeric columns
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            stock_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.table.setItem(row, 0, id_item)
            self.table.setItem(row, 1, name_item)
            self.table.setItem(row, 2, price_item)
            self.table.setItem(row, 3, stock_item)

            # Status with color
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
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.table.setItem(row, 4, status_item)

    # ---------------- STYLE ----------------
    def table_style(self):
        return """
            QTableWidget {
                background-color: #1E293B;
                color: #E2E8F0;
                border: 1px solid #2A3A55;
                border-radius: 8px;
                font-size: 13px;
                gridline-color: transparent;
            }

            QHeaderView::section {
                background-color: #273449;
                color: #F1F5F9;
                padding: 8px 12px;
                border: none;
                font-weight: bold;
                font-size: 13px;
                min-height: 22px;
            }

            QTableWidget::item {
                padding: 6px 10px;
                border-bottom: 1px solid #253045;
            }

            QTableWidget::item:selected {
                background-color: #3B82F6;
                color: #FFFFFF;
            }

            QTableWidget::item:alternate {
                background-color: #1a2d44;
            }

            QScrollBar:vertical {
                background-color: #1E293B;
                width: 8px;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical {
                background-color: #475569;
                border-radius: 4px;
                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover {
                background-color: #64748B;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical,
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
                border: none;
            }
        """