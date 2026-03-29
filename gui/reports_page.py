from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class ReportsPage(QWidget):

    def __init__(self, inventory_controller, sales_controller):
        super().__init__()

        self.inventory_controller = inventory_controller
        self.sales_controller = sales_controller

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()

        products = self.inventory_controller.get_all_products()
        sales = self.sales_controller.get_sales()

        text = "Products:\n"

        for p in products:
            text += f"{p['product_name']} - {p['stock_quantity']}\n"

        text += "\nSales:\n"

        for s in sales:
            text += f"{s['product_name']} - {s['total_price']}\n"

        layout.addWidget(QLabel(text))

        self.setLayout(layout)