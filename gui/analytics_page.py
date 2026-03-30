from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QHBoxLayout, QFrame, QTableWidget,
    QTableWidgetItem
)
from PyQt6.QtCore import Qt

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime


class AnalyticsPage(QWidget):

    def __init__(self, inventory_controller, sales_controller):
        super().__init__()

        self.inventory_controller = inventory_controller
        self.sales_controller = sales_controller

        self.init_ui()

    def init_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)

        # 🔥 TITLE
        title = QLabel("📊 Admin Dashboard")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(title)

        # ================= CARDS =================
        cards_layout = QHBoxLayout()

        self.products_card = self.create_card("Total Products")
        self.revenue_card = self.create_card("Total Revenue")
        self.transactions_card = self.create_card("Transactions")

        cards_layout.addWidget(self.products_card)
        cards_layout.addWidget(self.revenue_card)
        cards_layout.addWidget(self.transactions_card)

        main_layout.addLayout(cards_layout)

        # ================= CHART =================
        self.canvas = FigureCanvas(plt.Figure())
        main_layout.addWidget(self.canvas)

        # ================= TABLE =================
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Product", "Qty", "Total", "Date"]
        )

        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

        self.load_data()

    # ---------------- CARD ----------------
    def create_card(self, title):

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #3b3b5c;
                border-radius: 12px;
                padding: 15px;
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

    # ---------------- LOAD DATA ----------------
    def load_data(self):

        products = self.inventory_controller.get_all_products()
        sales = self.sales_controller.get_sales()

        total_products = len(products)
        total_revenue = sum(s.get("total_price", 0) for s in sales)
        total_transactions = len(sales)

        # 🔥 UPDATE CARDS
        self.products_card.value_label.setText(str(total_products))
        self.revenue_card.value_label.setText(f"₹{total_revenue}")
        self.transactions_card.value_label.setText(str(total_transactions))

        # 🔥 CHART
        self.plot_donut_chart(total_revenue, total_transactions, sales)

        # 🔥 TABLE
        self.load_table(sales)

    # ---------------- DONUT CHART ----------------
    def plot_donut_chart(self, revenue, transactions, sales):

        today = datetime.now().strftime("%Y-%m-%d")

        today_revenue = sum(
            s.get("total_price", 0)
            for s in sales
            if today in s.get("sale_date", "")
        )

        labels = ["Revenue", "Transactions", "Today"]
        values = [revenue, transactions, today_revenue]

        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)

        ax.pie(values, labels=labels, autopct='%1.1f%%')

        # 🔥 donut effect
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = self.canvas.figure
        fig.gca().add_artist(centre_circle)

        ax.set_title("Business Overview")

        self.canvas.draw()

    # ---------------- TABLE ----------------
    def load_table(self, sales):

        recent_sales = sales[-10:]  # last 10

        self.table.setRowCount(len(recent_sales))

        for row, s in enumerate(recent_sales):

            self.table.setItem(row, 0, QTableWidgetItem(s.get("product_name")))
            self.table.setItem(row, 1, QTableWidgetItem(str(s.get("quantity"))))
            self.table.setItem(row, 2, QTableWidgetItem(str(s.get("total_price"))))
            self.table.setItem(row, 3, QTableWidgetItem(s.get("sale_date")))

        self.table.resizeColumnsToContents()