from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox
)


class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Grocery Management System - Login")
        self.setGeometry(500, 200, 350, 250)

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout()

        # Title
        title = QLabel("Login")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        # Username field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter Username")
        layout.addWidget(self.username_input)

        # Password field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Login button
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def handle_login(self):

        username = self.username_input.text()
        password = self.password_input.text()

        # Temporary login validation
        if username == "admin" and password == "admin":

            QMessageBox.information(self, "Success", "Login Successful!")

        else:

            QMessageBox.warning(self, "Error", "Invalid username or password.")