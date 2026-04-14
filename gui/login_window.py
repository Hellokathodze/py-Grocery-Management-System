from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QFrame,
    QMessageBox, QGraphicsDropShadowEffect,
    QHBoxLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize
from PyQt6.QtGui import QColor, QFont, QIcon


class LoginWindow(QWidget):

    def __init__(self, auth_controller, inventory_controller, sales_controller, purchase_controller):
        super().__init__()

        self.setWindowTitle("Grocery Management System")
        self.setFixedSize(520, 620)

        # Controllers
        self.auth_controller = auth_controller
        self.inventory_controller = inventory_controller
        self.sales_controller = sales_controller
        self.purchase_controller = purchase_controller

        self.setStyleSheet(self.get_styles())
        self.init_ui()

    def init_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # ================= CARD =================
        card = QFrame()
        card.setObjectName("card")
        card.setFixedWidth(420)

        # Drop shadow on card
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 80))
        card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout()
        card_layout.setSpacing(8)
        card_layout.setContentsMargins(36, 40, 36, 36)

        # ================= LOGO / ICON =================
        logo_label = QLabel("🛒")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("font-size: 48px; background: transparent; border: none; padding: 0;")
        card_layout.addWidget(logo_label)

        # ================= TITLE =================
        title = QLabel("Welcome Back")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("title")
        card_layout.addWidget(title)

        subtitle = QLabel("Kailash General Store")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setObjectName("subtitle")
        card_layout.addWidget(subtitle)

        # Spacer
        card_layout.addSpacing(20)

        # ================= USERNAME =================
        username_label = QLabel("Username")
        username_label.setObjectName("fieldLabel")
        card_layout.addWidget(username_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setObjectName("inputField")
        self.username_input.setMinimumHeight(44)
        card_layout.addWidget(self.username_input)

        card_layout.addSpacing(6)

        # ================= PASSWORD =================
        password_label = QLabel("Password")
        password_label.setObjectName("fieldLabel")
        card_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setObjectName("inputField")
        self.password_input.setMinimumHeight(44)
        card_layout.addWidget(self.password_input)

        # Enter key login
        self.password_input.returnPressed.connect(self.handle_login)

        card_layout.addSpacing(16)

        # ================= LOGIN BUTTON =================
        self.login_button = QPushButton("Sign In")
        self.login_button.setObjectName("loginBtn")
        self.login_button.setMinimumHeight(46)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.clicked.connect(self.handle_login)
        card_layout.addWidget(self.login_button)

        card_layout.addSpacing(8)

        # ================= FOOTER =================
        footer = QLabel("Grocery Management System")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setObjectName("footer")
        card_layout.addWidget(footer)

        card.setLayout(card_layout)
        main_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

    # ---------------- LOGIN LOGIC ----------------
    def handle_login(self):

        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter all fields.")
            return

        self.login_button.setEnabled(False)
        self.login_button.setText("Signing in...")

        try:
            user = self.auth_controller.login(username, password)

            if user:
                QMessageBox.information(self, "Success", "Login Successful!")

                from gui.dashboard import DashboardWindow

                self.dashboard = DashboardWindow(
                    user,
                    self.inventory_controller,
                    self.sales_controller,
                    self.purchase_controller,
                    self.auth_controller
                )
                self.dashboard.show()
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Invalid username or password.")

        except Exception as e:
            print("LOGIN ERROR:", e)
            QMessageBox.critical(self, "Error", "Something went wrong!")

        finally:
            self.login_button.setEnabled(True)
            self.login_button.setText("Sign In")

    # ---------------- STYLES ----------------
    def get_styles(self):
        return """
        QWidget {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #0B1120,
                stop:0.5 #111D35,
                stop:1 #0F1B2E
            );
            color: #E2E8F0;
            font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
        }

        #card {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #1A2742,
                stop:1 #15203A
            );
            border-radius: 18px;
            border: 1px solid rgba(255, 255, 255, 25);
        }

        #title {
            font-size: 26px;
            font-weight: bold;
            color: #F8FAFC;
            padding: 0;
            margin: 0;
            background: transparent;
            border: none;
        }

        #subtitle {
            font-size: 13px;
            color: #64748B;
            padding: 0;
            background: transparent;
            border: none;
        }

        #fieldLabel {
            font-size: 12px;
            font-weight: bold;
            color: #94A3B8;
            padding: 0;
            background: transparent;
            border: none;
            letter-spacing: 0.5px;
        }

        #inputField {
            background-color: #0F1A2E;
            border: 1.5px solid #2A3A55;
            padding: 10px 14px;
            border-radius: 10px;
            color: #F1F5F9;
            font-size: 14px;
        }

        #inputField:focus {
            border: 1.5px solid #3B82F6;
            background-color: #111E36;
        }

        #inputField:hover {
            border: 1.5px solid #3B6ECF;
        }

        #loginBtn {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #2563EB,
                stop:1 #3B82F6
            );
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 15px;
            font-weight: bold;
            letter-spacing: 0.5px;
        }

        #loginBtn:hover {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #1D4ED8,
                stop:1 #2563EB
            );
        }

        #loginBtn:pressed {
            background-color: #1E40AF;
        }

        #loginBtn:disabled {
            background-color: #334155;
            color: #64748B;
        }

        #footer {
            font-size: 11px;
            color: #475569;
            padding-top: 4px;
            background: transparent;
            border: none;
        }

        QMessageBox {
            background-color: #1A2742;
            color: #E2E8F0;
        }

        QMessageBox QPushButton {
            background-color: #2563EB;
            border-radius: 6px;
            padding: 6px 20px;
            color: white;
        }
        """