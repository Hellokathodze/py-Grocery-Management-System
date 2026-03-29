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

        # 🔥 MAIN LAYOUT (FIXED)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 🔥 CARD (WIDER + CLEAN)
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #2c2c54;
                border-radius: 12px;
                padding: 30px;
            }
        """)
        card.setMaximumWidth(500)   # 🔥 better size

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

        # QUANTITY INPUT
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

        # ADD CARD TO MAIN LAYOUT
        main_layout.addWidget(card)

        self.setLayout(main_layout)

        self.load_products()

    def load_products(self):
        products = self.sales_controller.inventory_controller.get_all_products()
        for p in products:
            self.product_dropdown.addItem(p["product_id"])

    def sell(self):

        product_id = self.product_dropdown.currentText()
        qty = self.quantity.value()

        success = self.sales_controller.record_sale(product_id, qty)

        if success:
            QMessageBox.information(self, "Success", "Sale Completed")
        else:
            QMessageBox.warning(self, "Error", "Insufficient stock")