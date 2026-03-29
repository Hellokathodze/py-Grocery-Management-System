from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QFrame,
    QMessageBox
)
from PyQt6.QtCore import Qt


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Grocery Management System")
        self.setGeometry(500, 200, 400, 350)

        self.inventory_controller = None
        self.sales_controller = None
        self.purchase_controller = None
        self.auth_controller = None

        self.setStyleSheet(self.get_styles())

        self.init_ui()

    def init_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 🔥 CARD FRAME
        card = QFrame()
        card.setObjectName("card")

        card_layout = QVBoxLayout()
        card_layout.setSpacing(15)
        card_layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("Login")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("title")
        card_layout.addWidget(title)

        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        card_layout.addWidget(self.username_input)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        card_layout.addWidget(self.password_input)

        # Button
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.handle_login)
        card_layout.addWidget(login_button)

        card.setLayout(card_layout)
        main_layout.addWidget(card)

        self.setLayout(main_layout)

    def handle_login(self):

        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter all fields.")
            return

        user = self.auth_controller.login(username, password)

        if user:
            QMessageBox.information(self, "Success", "Login Successful!")

            from gui.dashboard import DashboardWindow

            self.dashboard = DashboardWindow(
                user,
                self.inventory_controller,
                self.sales_controller,
                self.purchase_controller
            )
            self.dashboard.show()
            self.close()

        else:
            QMessageBox.warning(self, "Error", "Invalid username or password.")

    def get_styles(self):
        return """
        QWidget {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #1e1e2f,
                stop:1 #2c2c54
            );
            color: white;
            font-family: Arial;
        }

        #card {
            background-color: #2f2f4f;
            border-radius: 15px;
            padding: 25px;
        }

        #title {
            font-size: 26px;
            font-weight: bold;
            padding: 10px 0px;
        }

        QLineEdit {
            background-color: #3b3b5c;
            border: none;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 10px;
            color: white;
        }

        QLineEdit:focus {
            border: 2px solid #6c63ff;
        }

        QPushButton {
            background-color: #6c63ff;
            border-radius: 10px;
            padding: 10px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #574fd6;
        }

        QPushButton:pressed {
            background-color: #4a43c4;
        }
        """