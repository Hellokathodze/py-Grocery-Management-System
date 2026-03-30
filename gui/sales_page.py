from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox,
    QPushButton, QMessageBox, QSpinBox, QFrame
)
from PyQt6.QtCore import Qt


class SalesPage(QWidget):

    def __init__(self, sales_controller):
        super().__init__()
        self.sales_controller = sales_controller
        self.init_ui()

    def init_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # CARD
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #2c2c54;
                border-radius: 12px;
                padding: 30px;
            }
        """)
        card.setMaximumWidth(500)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        # TITLE
        title = QLabel("💰 Sales")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        # PRODUCT DROPDOWN
        self.product_dropdown = QComboBox()
        self.product_dropdown.setMinimumHeight(35)
        layout.addWidget(self.product_dropdown)

        # QUANTITY
        self.quantity = QSpinBox()
        self.quantity.setMinimum(1)
        self.quantity.setMinimumHeight(35)
        layout.addWidget(self.quantity)

        # BUTTON
        btn = QPushButton("Sell Product")
        btn.setMinimumHeight(40)
        btn.clicked.connect(self.sell)
        layout.addWidget(btn)

        card.setLayout(layout)
        main_layout.addWidget(card)
        self.setLayout(main_layout)

        self.load_products()

    # ✅ FIXED: Fetch from SalesController → Service → DB
    def load_products(self):
        self.product_dropdown.clear()

        products = self.sales_controller.get_products()

        for p in products:
            display_text = f"{p['product_id']} - {p['product_name']}"
            self.product_dropdown.addItem(display_text)

    def sell(self):

        selected = self.product_dropdown.currentText()

        if not selected:
            QMessageBox.warning(self, "Error", "No product selected")
            return

        # ✅ Extract product_id
        product_id = selected.split(" - ")[0]
        qty = self.quantity.value()

        success = self.sales_controller.record_sale(product_id, qty)

        if success:
            QMessageBox.information(self, "Success", "Sale Completed")
        else:
            QMessageBox.warning(self, "Error", "Insufficient stock")