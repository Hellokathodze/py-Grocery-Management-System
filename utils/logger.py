from datetime import datetime
import os


class Logger:

    LOG_FILE = "logs/system.log"

    @staticmethod
    def log(message):

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        os.makedirs("logs", exist_ok=True)

        with open(Logger.LOG_FILE, "a", encoding="utf-8") as file:
            file.write(f"[{timestamp}] {message}\n")