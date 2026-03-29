import sys

from PyQt6.QtWidgets import QApplication, QMessageBox

# Import login window
from gui.login_window import LoginWindow


def main():
    try:
        # Create application
        app = QApplication(sys.argv)

        # Create login window
        window = LoginWindow()
        window.show()

        # Start GUI event loop
        sys.exit(app.exec())

    except Exception as e:
        # Show error popup if GUI fails
        error_box = QMessageBox()
        error_box.setWindowTitle("Application Error")
        error_box.setText("Failed to start the application.")
        error_box.setDetailedText(str(e))
        error_box.exec()


if __name__ == "__main__":
    main()