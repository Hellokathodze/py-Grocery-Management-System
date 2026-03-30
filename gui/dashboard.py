from PyQt6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout,
    QHBoxLayout, QLabel, QStackedWidget, QFrame
)
from PyQt6.QtCore import Qt

from gui.inventory_page import InventoryPage
from gui.sales_page import SalesPage
from gui.analytics_page import AnalyticsPage
from gui.manage_product_page import ManageProductPage   # 🔥 NEW


class DashboardWindow(QWidget):

    def __init__(self, user, inventory_controller, sales_controller, purchase_controller, auth_controller):
        super().__init__()

        self.user = user
        self.role = user.get("role", "admin")

        self.inventory_controller = inventory_controller
        self.sales_controller = sales_controller
        self.purchase_controller = purchase_controller
        self.auth_controller = auth_controller

        self.setWindowTitle("Dashboard - Grocery System")
        self.setGeometry(100, 50, 1200, 700)

        self.setStyleSheet(self.get_styles())

        self.init_ui()

    def init_ui(self):

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # ================= SIDEBAR =================
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(12)

        title = QLabel(f"👤 {self.user['username']}")
        title.setObjectName("sidebarTitle")

        role_badge = QLabel(self.role.upper())
        role_badge.setObjectName("roleBadge")

        sidebar_layout.addWidget(title)
        sidebar_layout.addWidget(role_badge)

        # ================= BUTTONS =================
        btn_inventory = QPushButton("📦 Inventory")
        btn_sales = QPushButton("💰 Billing")
        btn_manage = QPushButton("🛠 Manage Products")  # 🔥 NEW
        btn_analytics = QPushButton("📊 Analytics")
        btn_logout = QPushButton("🚪 Logout")

        # ================= ROLE BASED =================
        if self.role == "admin":
            self.menu_buttons = [btn_inventory, btn_manage, btn_sales, btn_analytics]
        else:
            self.menu_buttons = [btn_sales, btn_inventory]  # cashier

        for btn in self.menu_buttons:
            btn.setObjectName("menuBtn")
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        btn_logout.setObjectName("logoutBtn")
        sidebar_layout.addWidget(btn_logout)

        sidebar.setLayout(sidebar_layout)

        # ================= CONTENT =================
        content = QFrame()
        content.setObjectName("content")

        content_layout = QVBoxLayout()

        self.stack = QStackedWidget()

        # ================= PAGES =================
        self.inventory_page = InventoryPage(self.inventory_controller)
        self.sales_page = SalesPage(self.sales_controller)
        self.analytics_page = AnalyticsPage(self.inventory_controller, self.sales_controller)
        self.manage_page = ManageProductPage(self.inventory_controller)  # 🔥 NEW

        # ================= ADD BASED ON ROLE =================
        if self.role == "admin":
            self.stack.addWidget(self.inventory_page)
            self.stack.addWidget(self.manage_page)     # 🔥 NEW
            self.stack.addWidget(self.sales_page)
            self.stack.addWidget(self.analytics_page)
        else:
            self.stack.addWidget(self.sales_page)
            self.stack.addWidget(self.inventory_page)

        content_layout.addWidget(self.stack)
        content.setLayout(content_layout)

        # ================= CONNECTIONS =================
        btn_inventory.clicked.connect(lambda: self.switch_page(self.inventory_page, btn_inventory))
        btn_sales.clicked.connect(lambda: self.switch_page(self.sales_page, btn_sales))
        btn_analytics.clicked.connect(lambda: self.switch_page(self.analytics_page, btn_analytics))
        btn_manage.clicked.connect(lambda: self.switch_page(self.manage_page, btn_manage))  # 🔥 NEW
        btn_logout.clicked.connect(self.logout)

        # ================= DEFAULT =================
        self.set_active(self.menu_buttons[0])
        self.stack.setCurrentIndex(0)

        # ================= ADD =================
        main_layout.addWidget(sidebar, 1)
        main_layout.addWidget(content, 4)

        self.setLayout(main_layout)

    # ================= SWITCH =================
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

    # ================= LOGOUT =================
    def logout(self):
        from gui.login_window import LoginWindow

        self.login = LoginWindow(
            self.auth_controller,
            self.inventory_controller,
            self.sales_controller,
            self.purchase_controller
        )

        self.login.show()
        self.close()

    # ================= STYLES =================
    def get_styles(self):
        return """
        QWidget {
            background-color: #1e1e2f;
            color: white;
            font-family: Segoe UI;
        }

        #sidebar {
            background-color: #2c2c54;
            border-radius: 15px;
            padding: 20px;
        }

        #sidebarTitle {
            font-size: 20px;
            font-weight: bold;
        }

        #roleBadge {
            background-color: #6c63ff;
            padding: 6px;
            border-radius: 8px;
            font-size: 12px;
            margin-bottom: 15px;
            text-align: center;
        }

        #menuBtn {
            background-color: #3b3b5c;
            border-radius: 10px;
            padding: 12px;
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
            border-radius: 10px;
            padding: 12px;
        }

        #logoutBtn:hover {
            background-color: #e60000;
        }

        #content {
            background-color: #252542;
            border-radius: 15px;
            padding: 20px;
        }
        """