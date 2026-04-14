from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QMessageBox, QComboBox, QFrame, QHeaderView
)
from PyQt6.QtCore import Qt
from utils.signal_bus import signal_bus


class ManageProductPage(QWidget):

    def __init__(self, inventory_controller):
        super().__init__()
        self.inventory_controller = inventory_controller
        self.all_products = []
        self.init_ui()

    def init_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
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
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        main_layout.addWidget(title)

        # FORM CARD
        form_card = QFrame()
        form_card.setStyleSheet("""
            QFrame {
                background-color: #1E293B;
                border-radius: 12px;
                padding: 12px;
            }
        """)
        form_layout = QVBoxLayout()

        input_row = QHBoxLayout()

        self.id_input = self.create_input("Product ID")
        self.name_input = self.create_input("Name")
        self.category_input = self.create_input("Category")
        self.price_input = self.create_input("Price")
        self.stock_input = self.create_input("Stock")

        input_row.addWidget(self.id_input)
        input_row.addWidget(self.name_input)
        input_row.addWidget(self.category_input)
        input_row.addWidget(self.price_input)
        input_row.addWidget(self.stock_input)

        form_layout.addLayout(input_row)

        # BUTTONS
        btn_row = QHBoxLayout()

        add_btn = self.create_button("Add", "#22C55E")
        update_btn = self.create_button("Update", "#3B82F6")
        delete_btn = self.create_button("Delete", "#EF4444")

        add_btn.clicked.connect(self.add_product)
        update_btn.clicked.connect(self.update_product)
        delete_btn.clicked.connect(self.delete_product)

        btn_row.addWidget(add_btn)
        btn_row.addWidget(update_btn)
        btn_row.addWidget(delete_btn)

        form_layout.addLayout(btn_row)
        form_card.setLayout(form_layout)
        main_layout.addWidget(form_card)

        # FILTER BAR
        filter_row = QHBoxLayout()

        self.search_input = self.create_input("🔍 Search product...")
        self.search_input.textChanged.connect(self.apply_filters)

        self.category_filter = QComboBox()
        self.category_filter.setStyleSheet(self.dropdown_style())
        self.category_filter.currentTextChanged.connect(self.apply_filters)

        filter_row.addWidget(self.search_input)
        filter_row.addWidget(self.category_filter)

        main_layout.addLayout(filter_row)

        # TABLE CARD
        table_card = QFrame()
        table_card.setStyleSheet("""
            QFrame {
                background-color: #1E293B;
                border-radius: 12px;
                padding: 10px;
            }
        """)
        table_layout = QVBoxLayout()
        table_layout.setContentsMargins(0, 0, 0, 0)  # 🔥 FIX CLIPPING

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Name", "Category", "Price", "Stock"]
        )

        # ✅ FINAL HEADER FIX
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setMinimumHeight(45)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # ✅ ROW HEIGHT FIX (CRITICAL)
        self.table.verticalHeader().setDefaultSectionSize(40)

        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)

        self.table.setMinimumHeight(350)

        self.table.setStyleSheet(self.table_style())
        self.table.cellClicked.connect(self.fill_form)

        table_layout.addWidget(self.table)
        table_card.setLayout(table_layout)

        main_layout.addWidget(table_card)

        self.setLayout(main_layout)

        signal_bus.inventory_updated.connect(self.load_products)

        self.load_products()

    # ---------------- UI HELPERS ----------------
    def create_input(self, placeholder):
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border-radius: 8px;
                background-color: #334155;
                border: 1px solid #475569;
                color: white;
            }
        """)
        return input_field

    def create_button(self, text, color):
        btn = QPushButton(text)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                opacity: 0.85;
            }}
        """)
        return btn

    def dropdown_style(self):
        return """
            QComboBox {
                padding: 8px;
                border-radius: 8px;
                background-color: #334155;
                color: white;
                border: 1px solid #475569;
            }
        """

    def table_style(self):
        return """
            QTableWidget {
                background-color: #1E293B;
                color: #E2E8F0;
                border-radius: 8px;
            }

            QHeaderView::section {
                background-color: #334155;
                color: #E2E8F0;
                padding: 10px;
                border: none;
                font-weight: bold;
                height: 45px;
            }

            QTableWidget::item {
                padding: 8px;
            }

            QTableWidget::item:selected {
                background-color: #3B82F6;
            }
        """

    # ---------------- LOGIC ----------------
    def load_products(self):
        self.all_products = self.inventory_controller.get_all_products()
        self.populate_category_dropdown()
        self.apply_filters()

    def display_products(self, products):
        self.table.setRowCount(len(products))

        for row, p in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(p["product_id"]))
            self.table.setItem(row, 1, QTableWidgetItem(p["product_name"]))
            self.table.setItem(row, 2, QTableWidgetItem(p.get("category", "")))
            self.table.setItem(row, 3, QTableWidgetItem(str(p["price"])))
            self.table.setItem(row, 4, QTableWidgetItem(str(p["stock_quantity"])))

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

    def fill_form(self, row, column):
        self.id_input.setText(self.table.item(row, 0).text())
        self.name_input.setText(self.table.item(row, 1).text())
        self.category_input.setText(self.table.item(row, 2).text())
        self.price_input.setText(self.table.item(row, 3).text())
        self.stock_input.setText(self.table.item(row, 4).text())

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
            signal_bus.inventory_updated.emit()

            QMessageBox.information(self, "Success", "Product added")

        except:
            QMessageBox.warning(self, "Error", "Invalid input!")

    def update_product(self):
        if not self.id_input.text():
            QMessageBox.warning(self, "Error", "Select a product!")
            return

        try:
            self.inventory_controller.update_product(
                self.id_input.text(),
                {
                    "product_name": self.name_input.text(),
                    "category": self.category_input.text(),
                    "price": float(self.price_input.text()),
                    "stock_quantity": int(self.stock_input.text())
                }
            )

            signal_bus.inventory_updated.emit()
            QMessageBox.information(self, "Updated", "Product updated")

        except:
            QMessageBox.warning(self, "Error", "Invalid input!")

    def delete_product(self):
        if not self.id_input.text():
            QMessageBox.warning(self, "Error", "Select a product!")
            return

        self.inventory_controller.delete_product(self.id_input.text())
        signal_bus.inventory_updated.emit()
        QMessageBox.information(self, "Deleted", "Product removed")