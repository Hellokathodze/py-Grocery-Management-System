from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame


class AnalyticsPage(QWidget):

    def __init__(self, inventory_controller, sales_controller):
        super().__init__()
        self.inventory_controller = inventory_controller
        self.sales_controller = sales_controller
        self.init_ui()

    def init_ui(self):

        main_layout = QVBoxLayout()

        title = QLabel("📊 Analytics")
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        main_layout.addWidget(title)

        # 🔥 CARD CONTAINER
        cards_layout = QHBoxLayout()

        self.products_card = self.create_card("Total Products")
        self.stock_card = self.create_card("Total Stock")
        self.revenue_card = self.create_card("Total Revenue")

        cards_layout.addWidget(self.products_card)
        cards_layout.addWidget(self.stock_card)
        cards_layout.addWidget(self.revenue_card)

        main_layout.addLayout(cards_layout)

        self.setLayout(main_layout)

        self.load_data()

    def create_card(self, title):

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #3b3b5c;
                border-radius: 12px;
                padding: 20px;
            }
        """)

        layout = QVBoxLayout()

        label_title = QLabel(title)
        label_title.setStyleSheet("font-size: 14px;")

        value = QLabel("0")
        value.setStyleSheet("font-size: 22px; font-weight: bold;")

        layout.addWidget(label_title)
        layout.addWidget(value)

        card.setLayout(layout)
        card.value_label = value

        return card

    def load_data(self):

        products = self.inventory_controller.get_all_products()
        sales = self.sales_controller.get_sales_analytics()

        self.products_card.value_label.setText(str(len(products)))
        self.stock_card.value_label.setText(
            str(sum(p.get("stock_quantity", 0) for p in products))
        )
        self.revenue_card.value_label.setText(
            f"₹{sales.get('total_revenue', 0)}"
        )