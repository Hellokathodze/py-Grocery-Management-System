from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QMessageBox, QComboBox, QFrame,
    QHeaderView, QAbstractItemView, QSizePolicy,
    QDateEdit, QGridLayout
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
from utils.signal_bus import signal_bus
from datetime import datetime


class ManageProductPage(QWidget):

    def __init__(self, inventory_controller):
        super().__init__()
        self.inventory_controller = inventory_controller
        self.all_products = []
        self.init_ui()

    def init_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setSpacing(14)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # GLOBAL STYLE
        self.setStyleSheet("""
            QWidget {
                background-color: #0F172A;
                color: #E2E8F0;
                font-size: 13px;
            }
        """)

        # TITLE
        title = QLabel("🛠 Manage Products")
        title.setStyleSheet(
            "font-size: 22px; font-weight: bold; color: #F1F5F9; "
            "background: transparent; border: none;"
        )
        main_layout.addWidget(title)

        # ================= FORM CARD =================
        form_card = QFrame()
        form_card.setObjectName("formCard")
        form_card.setStyleSheet("""
            QFrame#formCard {
                background-color: #1E293B;
                border-radius: 12px;
            }
        """)

        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(18, 16, 18, 16)
        form_layout.setSpacing(12)

        # Row 1: ID, Name, Category
        row1 = QHBoxLayout()
        row1.setSpacing(10)

        self.id_input = self.create_input("Product ID")
        self.name_input = self.create_input("Product Name")
        self.category_input = self.create_input("Category")

        row1.addWidget(self.create_field("ID", self.id_input))
        row1.addWidget(self.create_field("Name", self.name_input))
        row1.addWidget(self.create_field("Category", self.category_input))

        form_layout.addLayout(row1)

        # Row 2: Price, Stock, Reorder Level, Expiry Date
        row2 = QHBoxLayout()
        row2.setSpacing(10)

        self.price_input = self.create_input("Price (₹)")
        self.stock_input = self.create_input("Stock Qty")
        self.reorder_input = self.create_input("Reorder Level")

        self.expiry_input = QDateEdit()
        self.expiry_input.setCalendarPopup(True)
        self.expiry_input.setDate(QDate.currentDate().addMonths(6))
        self.expiry_input.setDisplayFormat("yyyy-MM-dd")
        self.expiry_input.setMinimumHeight(38)
        self.expiry_input.setStyleSheet(self.date_input_style())

        row2.addWidget(self.create_field("Price (₹)", self.price_input))
        row2.addWidget(self.create_field("Stock", self.stock_input))
        row2.addWidget(self.create_field("Reorder Lvl", self.reorder_input))
        row2.addWidget(self.create_field("Expiry Date", self.expiry_input))

        form_layout.addLayout(row2)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        add_btn = self.create_button("➕ Add", "#22C55E")
        update_btn = self.create_button("✏️ Update", "#3B82F6")
        delete_btn = self.create_button("🗑️ Delete", "#EF4444")
        clear_btn = self.create_button("🔄 Clear", "#64748B")

        add_btn.clicked.connect(self.add_product)
        update_btn.clicked.connect(self.update_product)
        delete_btn.clicked.connect(self.delete_product)
        clear_btn.clicked.connect(self.clear_form)

        btn_row.addWidget(add_btn)
        btn_row.addWidget(update_btn)
        btn_row.addWidget(delete_btn)
        btn_row.addWidget(clear_btn)

        form_layout.addLayout(btn_row)

        form_card.setLayout(form_layout)
        main_layout.addWidget(form_card)

        # ================= FILTER BAR =================
        filter_row = QHBoxLayout()
        filter_row.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search product...")
        self.search_input.setMinimumHeight(38)
        self.search_input.setStyleSheet(self.search_style())
        self.search_input.textChanged.connect(self.apply_filters)

        self.category_filter = QComboBox()
        self.category_filter.setMinimumHeight(38)
        self.category_filter.setMinimumWidth(140)
        self.category_filter.setStyleSheet(self.dropdown_style())
        self.category_filter.currentTextChanged.connect(self.apply_filters)

        filter_row.addWidget(self.search_input, 4)
        filter_row.addWidget(self.category_filter, 1)

        main_layout.addLayout(filter_row)

        # ================= TABLE =================
        table_card = QFrame()
        table_card.setObjectName("tableCard")
        table_card.setStyleSheet("""
            QFrame#tableCard {
                background-color: #1E293B;
                border-radius: 12px;
            }
        """)

        table_layout = QVBoxLayout()
        table_layout.setContentsMargins(12, 12, 12, 12)
        table_layout.setSpacing(0)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Name", "Category", "Price (₹)",
             "Stock", "Reorder Lvl", "Expiry Date", "Expiry Status"]
        )

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setStretchLastSection(True)
        header.setMinimumHeight(40)
        header.setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        self.table.verticalHeader().setDefaultSectionSize(40)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.table.setMinimumHeight(300)

        self.table.setStyleSheet(self.table_style())
        self.table.cellClicked.connect(self.fill_form)

        table_layout.addWidget(self.table)
        table_card.setLayout(table_layout)

        main_layout.addWidget(table_card)

        self.setLayout(main_layout)

        signal_bus.inventory_updated.connect(self.load_products)

        self.load_products()

    # ================= UI HELPERS =================
    def create_field(self, label_text, widget):
        """Wraps an input widget with a small label above it."""
        container = QWidget()
        container.setStyleSheet("background: transparent; border: none;")
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        label = QLabel(label_text)
        label.setStyleSheet(
            "font-size: 11px; color: #64748B; font-weight: bold; "
            "letter-spacing: 0.5px; background: transparent; border: none;"
        )
        layout.addWidget(label)
        layout.addWidget(widget)

        container.setLayout(layout)
        return container

    def create_input(self, placeholder):
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        field.setMinimumHeight(38)
        field.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border-radius: 8px;
                background-color: #0F172A;
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
        return field

    def create_button(self, text, color):
        btn = QPushButton(text)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumHeight(40)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                padding: 10px 16px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {color}CC;
            }}
            QPushButton:pressed {{
                background-color: {color}AA;
            }}
        """)
        return btn

    def date_input_style(self):
        return """
            QDateEdit {
                padding: 8px 12px;
                border-radius: 8px;
                background-color: #0F172A;
                border: 1.5px solid #2A3A55;
                color: white;
                font-size: 13px;
            }
            QDateEdit:focus {
                border: 1.5px solid #3B82F6;
            }
            QDateEdit::drop-down {
                border: none;
                padding-right: 8px;
            }
            QDateEdit::down-arrow {
                width: 12px;
                height: 12px;
            }
            QCalendarWidget {
                background-color: #1E293B;
                color: #E2E8F0;
            }
            QCalendarWidget QToolButton {
                color: white;
                background-color: #334155;
                border-radius: 4px;
                padding: 4px;
            }
            QCalendarWidget QMenu {
                background-color: #1E293B;
                color: white;
            }
        """

    def search_style(self):
        return """
            QLineEdit {
                padding: 8px 14px;
                border-radius: 10px;
                background-color: #0F172A;
                border: 1.5px solid #2A3A55;
                color: white;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1.5px solid #3B82F6;
                background-color: #111E36;
            }
        """

    def dropdown_style(self):
        return """
            QComboBox {
                padding: 8px 12px;
                border-radius: 8px;
                background-color: #0F172A;
                color: white;
                border: 1.5px solid #2A3A55;
                font-size: 13px;
            }
            QComboBox:hover {
                border: 1.5px solid #3B6ECF;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: #334155;
                color: white;
                selection-background-color: #3B82F6;
                border: 1px solid #475569;
                border-radius: 4px;
            }
        """

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
                padding: 8px 10px;
                border: none;
                font-weight: bold;
                font-size: 12px;
                min-height: 22px;
            }

            QTableWidget::item {
                padding: 6px 8px;
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

            QScrollBar:horizontal {
                background-color: #1E293B;
                height: 8px;
                border-radius: 4px;
            }

            QScrollBar::handle:horizontal {
                background-color: #475569;
                border-radius: 4px;
                min-width: 30px;
            }

            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal,
            QScrollBar::add-page:horizontal,
            QScrollBar::sub-page:horizontal {
                background: none;
                border: none;
            }
        """

    # ================= DATA LOGIC =================
    def load_products(self):
        self.all_products = self.inventory_controller.get_products_with_expiry_status()
        self.populate_category_dropdown()
        self.apply_filters()

    def display_products(self, products):
        self.table.setRowCount(len(products))
        today = datetime.now().date()

        for row, p in enumerate(products):
            price = p.get("price", 0)
            stock = p.get("stock_quantity", 0)
            reorder = p.get("reorder_level", 0)
            expiry_date = p.get("expiry_date", "")
            expiry_status = p.get("expiry_status", "no_date")
            days_remaining = p.get("days_remaining", None)

            id_item = QTableWidgetItem(str(p.get("product_id", "")))
            name_item = QTableWidgetItem(p.get("product_name", ""))
            cat_item = QTableWidgetItem(p.get("category", ""))
            price_item = QTableWidgetItem(f"₹{price:,.2f}")
            stock_item = QTableWidgetItem(str(stock))
            reorder_item = QTableWidgetItem(str(reorder))
            expiry_date_item = QTableWidgetItem(str(expiry_date) if expiry_date else "N/A")

            # Center align
            for item in [id_item, price_item, stock_item, reorder_item, expiry_date_item]:
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.table.setItem(row, 0, id_item)
            self.table.setItem(row, 1, name_item)
            self.table.setItem(row, 2, cat_item)
            self.table.setItem(row, 3, price_item)
            self.table.setItem(row, 4, stock_item)
            self.table.setItem(row, 5, reorder_item)
            self.table.setItem(row, 6, expiry_date_item)

            # Color expiry date
            if expiry_status == "expired":
                expiry_date_item.setForeground(QColor("#EF4444"))
            elif expiry_status == "expiring_soon":
                expiry_date_item.setForeground(QColor("#F59E0B"))

            # Stock color: red if below reorder level
            if stock <= reorder and stock > 0:
                stock_item.setForeground(QColor("#F59E0B"))
            elif stock == 0:
                stock_item.setForeground(QColor("#EF4444"))

            # Expiry status column
            if expiry_status == "expired":
                expiry_text = f"🔴 Expired ({abs(days_remaining)}d ago)"
                expiry_color = "#EF4444"
            elif expiry_status == "expiring_soon":
                expiry_text = f"🟡 {days_remaining}d left"
                expiry_color = "#F59E0B"
            elif expiry_status == "ok":
                expiry_text = f"🟢 {days_remaining}d left"
                expiry_color = "#22C55E"
            else:
                expiry_text = "—"
                expiry_color = "#475569"

            expiry_status_item = QTableWidgetItem(expiry_text)
            expiry_status_item.setForeground(QColor(expiry_color))
            expiry_status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 7, expiry_status_item)

            # Highlight expired rows
            if expiry_status == "expired":
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    if item:
                        item.setBackground(QColor("#2D1515"))

    def populate_category_dropdown(self):
        self.category_filter.blockSignals(True)
        self.category_filter.clear()
        self.category_filter.addItem("All")

        categories = set(
            p.get("category", "") for p in self.all_products if p.get("category")
        )
        for cat in sorted(categories):
            self.category_filter.addItem(cat)

        self.category_filter.blockSignals(False)

    def apply_filters(self):
        search = self.search_input.text().lower()
        category = self.category_filter.currentText()

        filtered = [
            p for p in self.all_products
            if search in p.get("product_name", "").lower()
            and (category == "All" or p.get("category") == category)
        ]

        self.display_products(filtered)

    # ================= FILL FORM ON CLICK =================
    def fill_form(self, row, column):
        self.id_input.setText(self.table.item(row, 0).text())
        self.name_input.setText(self.table.item(row, 1).text())
        self.category_input.setText(self.table.item(row, 2).text())

        # Strip ₹ and commas from price
        price_text = self.table.item(row, 3).text().replace("₹", "").replace(",", "")
        self.price_input.setText(price_text)

        self.stock_input.setText(self.table.item(row, 4).text())
        self.reorder_input.setText(self.table.item(row, 5).text())

        # Set expiry date
        expiry_text = self.table.item(row, 6).text()
        if expiry_text and expiry_text != "N/A":
            try:
                date = QDate.fromString(expiry_text[:10], "yyyy-MM-dd")
                if date.isValid():
                    self.expiry_input.setDate(date)
            except Exception:
                pass

        # Lock ID field on edit (can't change product ID)
        self.id_input.setReadOnly(True)
        self.id_input.setStyleSheet(
            self.id_input.styleSheet() +
            "QLineEdit { color: #64748B; }"
        )

    # ================= CLEAR FORM =================
    def clear_form(self):
        self.id_input.clear()
        self.name_input.clear()
        self.category_input.clear()
        self.price_input.clear()
        self.stock_input.clear()
        self.reorder_input.clear()
        self.expiry_input.setDate(QDate.currentDate().addMonths(6))

        # Unlock ID field
        self.id_input.setReadOnly(False)
        self.id_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border-radius: 8px;
                background-color: #0F172A;
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

    # ================= ADD =================
    def add_product(self):
        if not self.id_input.text().strip():
            QMessageBox.warning(self, "Error", "Product ID is required!")
            return

        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Error", "Product Name is required!")
            return

        try:
            data = {
                "product_id": self.id_input.text().strip(),
                "product_name": self.name_input.text().strip(),
                "category": self.category_input.text().strip(),
                "price": float(self.price_input.text()),
                "stock_quantity": int(self.stock_input.text()),
                "reorder_level": int(self.reorder_input.text()) if self.reorder_input.text().strip() else 10,
                "expiry_date": self.expiry_input.date().toString("yyyy-MM-dd")
            }

            success = self.inventory_controller.add_product(data)

            if success:
                signal_bus.inventory_updated.emit()
                self.clear_form()
                QMessageBox.information(self, "Success", "Product added successfully!")
            else:
                QMessageBox.warning(self, "Error", "Product ID already exists!")

        except ValueError:
            QMessageBox.warning(self, "Error", "Price and Stock must be valid numbers!")

    # ================= UPDATE =================
    def update_product(self):
        if not self.id_input.text().strip():
            QMessageBox.warning(self, "Error", "Select a product first!")
            return

        try:
            updated_data = {
                "product_name": self.name_input.text().strip(),
                "category": self.category_input.text().strip(),
                "price": float(self.price_input.text()),
                "stock_quantity": int(self.stock_input.text()),
                "reorder_level": int(self.reorder_input.text()) if self.reorder_input.text().strip() else 10,
                "expiry_date": self.expiry_input.date().toString("yyyy-MM-dd")
            }

            success = self.inventory_controller.update_product(
                self.id_input.text().strip(), updated_data
            )

            if success:
                signal_bus.inventory_updated.emit()
                self.clear_form()
                QMessageBox.information(self, "Success", "Product updated successfully!")
            else:
                QMessageBox.warning(self, "Error", "Product not found!")

        except ValueError:
            QMessageBox.warning(self, "Error", "Price and Stock must be valid numbers!")

    # ================= DELETE =================
    def delete_product(self):
        product_id = self.id_input.text().strip()

        if not product_id:
            QMessageBox.warning(self, "Error", "Select a product first!")
            return

        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete product '{product_id}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            success = self.inventory_controller.delete_product(product_id)

            if success:
                signal_bus.inventory_updated.emit()
                self.clear_form()
                QMessageBox.information(self, "Deleted", "Product removed successfully!")
            else:
                QMessageBox.warning(self, "Error", "Product not found!")