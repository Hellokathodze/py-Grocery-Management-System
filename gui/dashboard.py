from PyQt6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout,
    QHBoxLayout, QLabel, QStackedWidget, QFrame
)
from PyQt6.QtCore import Qt

from gui.inventory_page import InventoryPage
from gui.sales_page import SalesPage
from gui.analytics_page import AnalyticsPage


class DashboardWindow(QWidget):

    def __init__(self, user, inventory_controller, sales_controller, purchase_controller):
        super().__init__()

        self.user = user
        self.inventory_controller = inventory_controller
        self.sales_controller = sales_controller
        self.purchase_controller = purchase_controller

        self.setWindowTitle("Dashboard - Grocery System")
        self.setGeometry(200, 100, 1000, 600)

        self.setStyleSheet(self.get_styles())

        self.init_ui()

    def init_ui(self):

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 🔥 SIDEBAR
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(15)

        # 🔥 FIXED HEADER
        title = QLabel(f"👤 Welcome,\n{self.user['username']}")
        title.setObjectName("sidebarTitle")
        title.setStyleSheet("background: transparent;")

        btn_inventory = QPushButton("📦 Inventory")
        btn_sales = QPushButton("💰 Sales")
        btn_analytics = QPushButton("📊 Analytics")
        btn_logout = QPushButton("🚪 Logout")

        self.menu_buttons = [btn_inventory, btn_sales, btn_analytics]

        for btn in self.menu_buttons:
            btn.setObjectName("menuBtn")
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        btn_logout.setObjectName("logoutBtn")
        sidebar_layout.addWidget(btn_logout)

        sidebar.setLayout(sidebar_layout)

        # 🔥 CONTENT AREA
        content = QFrame()
        content.setObjectName("content")

        content_layout = QVBoxLayout()

        self.stack = QStackedWidget()

        self.inventory_page = InventoryPage(self.inventory_controller)
        self.sales_page = SalesPage(self.sales_controller)
        self.analytics_page = AnalyticsPage(self.inventory_controller, self.sales_controller)

        self.stack.addWidget(self.inventory_page)
        self.stack.addWidget(self.sales_page)
        self.stack.addWidget(self.analytics_page)

        content_layout.addWidget(self.stack)
        content.setLayout(content_layout)

        # 🔥 BUTTON CONNECTIONS + ACTIVE STATE
        btn_inventory.clicked.connect(lambda: self.switch_page(self.inventory_page, btn_inventory))
        btn_sales.clicked.connect(lambda: self.switch_page(self.sales_page, btn_sales))
        btn_analytics.clicked.connect(lambda: self.switch_page(self.analytics_page, btn_analytics))
        btn_logout.clicked.connect(self.logout)

        # DEFAULT ACTIVE BUTTON
        self.set_active(btn_inventory)

        # ADD TO MAIN
        main_layout.addWidget(sidebar, 1)
        main_layout.addWidget(content, 4)

        self.setLayout(main_layout)

    # 🔥 PAGE SWITCH WITH ACTIVE HIGHLIGHT
    def switch_page(self, page, button):
        self.stack.setCurrentWidget(page)
        self.set_active(button)

    def set_active(self, active_btn):
        for btn in self.menu_buttons:
            btn.setProperty("active", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        active_btn.setProperty("active", True)
        active_btn.style().unpolish(active_btn)
        active_btn.style().polish(active_btn)

    def logout(self):
        from gui.login_window import LoginWindow
        self.login = LoginWindow()
        self.login.show()
        self.close()

    def get_styles(self):
        return """
        QWidget {
            background-color: #1e1e2f;
            color: white;
            font-family: Arial;
        }

        #sidebar {
            background-color: #2c2c54;
            border-radius: 12px;
            padding: 20px;
        }

        #sidebarTitle {
            font-size: 20px;
            font-weight: bold;
            padding: 10px;
            margin-bottom: 15px;
            background: transparent;
            border: none;
        }

        #menuBtn {
            background-color: #3b3b5c;
            border-radius: 8px;
            padding: 10px;
            text-align: left;
        }

        #menuBtn:hover {
            background-color: #6c63ff;
        }

        #menuBtn[active="true"] {
            background-color: #6c63ff;
            font-weight: bold;
        }

        #logoutBtn {
            background-color: #ff4d4d;
            border-radius: 8px;
            padding: 10px;
        }

        #logoutBtn:hover {
            background-color: #e60000;
        }

        #content {
            background-color: #252542;
            border-radius: 12px;
            padding: 20px;
        }
        """