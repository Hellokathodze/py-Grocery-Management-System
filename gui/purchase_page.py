from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QFrame
from PyQt6.QtCore import Qt


class PurchasePage(QWidget):

    def __init__(self, purchase_controller):
        super().__init__()
        self.purchase_controller = purchase_controller
        self.init_ui()

    def init_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #2c2c54;
                border-radius: 12px;
                padding: 25px;
                max-width: 350px;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        title = QLabel("🛒 Purchase")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        self.product_id_input = QComboBox()
        layout.addWidget(self.product_id_input)

        btn = QPushButton("Add Stock")
        btn.clicked.connect(self.add_purchase)
        layout.addWidget(btn)

        card.setLayout(layout)
        main_layout.addWidget(card)

        self.setLayout(main_layout)

        self.load_products()

    def load_products(self):
        products = self.purchase_controller.inventory_controller.get_all_products()
        for p in products:
            self.product_id_input.addItem(p["product_id"])

    def add_purchase(self):
        product_id = self.product_id_input.currentText()
        self.purchase_controller.record_purchase(product_id, 5, 50)
        QMessageBox.information(self, "Success", "Stock Added")