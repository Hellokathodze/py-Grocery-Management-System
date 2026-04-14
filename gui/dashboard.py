from PyQt6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout,
    QHBoxLayout, QLabel, QStackedWidget,
    QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from gui.inventory_page import InventoryPage
from gui.sales_page import SalesPage
from gui.analytics_page import AnalyticsPage
from gui.manage_product_page import ManageProductPage


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
        self.setMinimumSize(1050, 680)
        self.resize(1250, 750)

        self.setStyleSheet(self.get_styles())
        self.init_ui()

    def init_ui(self):

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ================= SIDEBAR =================
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(250)

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(16, 20, 16, 20)
        sidebar_layout.setSpacing(6)

        # Brand header
        brand_frame = QFrame()
        brand_frame.setObjectName("brandFrame")
        brand_layout = QVBoxLayout()
        brand_layout.setContentsMargins(12, 12, 12, 12)
        brand_layout.setSpacing(4)

        brand_icon = QLabel(" 🛒 ")
        brand_icon.setStyleSheet("font-size: 28px; background: transparent; border: none;")

        brand_name = QLabel("KailashGeneralStore")
        brand_name.setObjectName("brandName")

        brand_layout.addWidget(brand_icon)
        brand_layout.addWidget(brand_name)
        brand_frame.setLayout(brand_layout)

        sidebar_layout.addWidget(brand_frame)
        sidebar_layout.addSpacing(8)

        # User info
        user_frame = QFrame()
        user_frame.setObjectName("userFrame")
        user_layout = QHBoxLayout()
        user_layout.setContentsMargins(12, 10, 12, 10)
        user_layout.setSpacing(10)

        avatar = QLabel("👤")
        avatar.setStyleSheet("font-size: 22px; background: transparent; border: none;")

        user_info_layout = QVBoxLayout()
        user_info_layout.setSpacing(2)

        user_name = QLabel(self.user['username'].title())
        user_name.setObjectName("userName")

        role_badge = QLabel(self.role.upper())
        role_badge.setObjectName("roleBadge")

        user_info_layout.addWidget(user_name)
        user_info_layout.addWidget(role_badge)

        user_layout.addWidget(avatar)
        user_layout.addLayout(user_info_layout)
        user_layout.addStretch()
        user_frame.setLayout(user_layout)

        sidebar_layout.addWidget(user_frame)
        sidebar_layout.addSpacing(16)

        # Nav section label
        nav_label = QLabel("NAVIGATION")
        nav_label.setObjectName("navLabel")
        sidebar_layout.addWidget(nav_label)
        sidebar_layout.addSpacing(4)

        # Navigation buttons
        btn_inventory = self.create_nav_btn("📦", "Inventory")
        btn_manage = self.create_nav_btn("🛠", "Manage Products")
        btn_sales = self.create_nav_btn("💰", "Billing")
        btn_analytics = self.create_nav_btn("📊", "Analytics")

        if self.role == "admin":
            self.menu_buttons = [btn_inventory, btn_manage, btn_sales, btn_analytics]
        else:
            self.menu_buttons = [btn_sales, btn_inventory]

        for btn in self.menu_buttons:
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # Logout button
        btn_logout = QPushButton("  🚪  Log Out")
        btn_logout.setObjectName("logoutBtn")
        btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_logout.setMinimumHeight(42)
        btn_logout.clicked.connect(self.logout)

        sidebar_layout.addWidget(btn_logout)

        sidebar.setLayout(sidebar_layout)

        # ================= CONTENT AREA =================
        content_wrapper = QFrame()
        content_wrapper.setObjectName("contentWrapper")

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(0)

        self.stack = QStackedWidget()

        self.inventory_page = InventoryPage(self.inventory_controller)
        self.sales_page = SalesPage(self.sales_controller)
        self.analytics_page = AnalyticsPage(self.inventory_controller, self.sales_controller)
        self.manage_page = ManageProductPage(self.inventory_controller)

        if self.role == "admin":
            self.stack.addWidget(self.inventory_page)
            self.stack.addWidget(self.manage_page)
            self.stack.addWidget(self.sales_page)
            self.stack.addWidget(self.analytics_page)
        else:
            self.stack.addWidget(self.sales_page)
            self.stack.addWidget(self.inventory_page)

        content_layout.addWidget(self.stack)
        content_wrapper.setLayout(content_layout)

        # Connect buttons
        btn_inventory.clicked.connect(lambda: self.switch_page(self.inventory_page, btn_inventory))
        btn_sales.clicked.connect(lambda: self.switch_page(self.sales_page, btn_sales))
        btn_analytics.clicked.connect(lambda: self.switch_page(self.analytics_page, btn_analytics))
        btn_manage.clicked.connect(lambda: self.switch_page(self.manage_page, btn_manage))

        # Set default active
        self.set_active(self.menu_buttons[0])
        self.stack.setCurrentIndex(0)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content_wrapper, 1)

        self.setLayout(main_layout)

    # ================= NAV BUTTON FACTORY =================
    def create_nav_btn(self, icon, text):
        btn = QPushButton(f"  {icon}   {text}")
        btn.setObjectName("navBtn")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumHeight(42)
        return btn

    # ================= PAGE SWITCHING =================
    def switch_page(self, page, button):
        self.stack.setCurrentWidget(page)
        self.set_active(button)

        # Refresh data when switching to analytics
        if page == self.analytics_page:
            self.analytics_page.load_data()

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
        * {
            font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
        }

        QWidget {
            background-color: #0B1120;
            color: #E2E8F0;
        }

        /* ===== SIDEBAR ===== */
        #sidebar {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #111D35,
                stop:1 #0E1829
            );
            border-right: 1px solid #1C2E4A;
        }

        #brandFrame {
            background: transparent;
            border: none;
            border-bottom: 1px solid #1C2E4A;
            padding-bottom: 12px;
        }

        #brandName {
            font-size: 20px;
            font-weight: bold;
            color: #F1F5F9;
            background: transparent;
            border: none;
        }

        #userFrame {
            background-color: #152039;
            border-radius: 10px;
            border: 1px solid #1E3050;
        }

        #userName {
            font-size: 14px;
            font-weight: bold;
            color: #E2E8F0;
            background: transparent;
            border: none;
        }

        #roleBadge {
            font-size: 10px;
            font-weight: bold;
            color: #60A5FA;
            background: transparent;
            border: none;
            letter-spacing: 1px;
        }

        #navLabel {
            font-size: 10px;
            font-weight: bold;
            color: #4B6A9B;
            letter-spacing: 1.5px;
            padding-left: 12px;
            background: transparent;
            border: none;
        }

        /* ===== NAV BUTTONS ===== */
        #navBtn {
            background-color: transparent;
            border: none;
            border-radius: 10px;
            padding: 10px 14px;
            text-align: left;
            font-size: 13px;
            font-weight: 500;
            color: #8899B4;
        }

        #navBtn:hover {
            background-color: #152039;
            color: #CBD5E1;
        }

        #navBtn[active="true"] {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #1E3A5F,
                stop:1 #1A2F4E
            );
            color: #60A5FA;
            font-weight: bold;
            border-left: 3px solid #3B82F6;
        }

        /* ===== LOGOUT ===== */
        #logoutBtn {
            background-color: #DC2626;
            border: none;
            border-radius: 10px;
            padding: 10px 14px;
            text-align: left;
            font-size: 13px;
            color: #FFFFFF;
            font-weight: bold;
        }

        #logoutBtn:hover {
            background-color: #EF4444;
        }

        #logoutBtn:pressed {
            background-color: #B91C1C;
        }

        /* ===== CONTENT AREA ===== */
        #contentWrapper {
            background-color: #0F172A;
            border-top-left-radius: 20px;
            border-bottom-left-radius: 20px;
        }

        /* ===== SCROLLBAR (GLOBAL) ===== */
        QScrollBar:vertical {
            background-color: #0F172A;
            width: 8px;
            border-radius: 4px;
        }

        QScrollBar::handle:vertical {
            background-color: #334155;
            border-radius: 4px;
            min-height: 30px;
        }

        QScrollBar::handle:vertical:hover {
            background-color: #475569;
        }

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical,
        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {
            background: none;
            border: none;
        }

        /* ===== MESSAGE BOXES ===== */
        QMessageBox {
            background-color: #1A2742;
            color: #E2E8F0;
        }

        QMessageBox QPushButton {
            background-color: #2563EB;
            border-radius: 6px;
            padding: 6px 20px;
            color: white;
            border: none;
        }

        QMessageBox QPushButton:hover {
            background-color: #1D4ED8;
        }
        """