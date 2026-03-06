import json
import os
from database.db_connection import DatabaseConnection


class BackupUtils:

    BACKUP_FOLDER = "backups"
    BACKUP_FILE = "backups/backup.json"

    @staticmethod
    def backup_database():

        os.makedirs(BackupUtils.BACKUP_FOLDER, exist_ok=True)

        db = DatabaseConnection().get_database()

        data = {
            "products": list(db.products.find({}, {"_id": 0})),
            "sales": list(db.sales.find({}, {"_id": 0})),
            "purchases": list(db.purchases.find({}, {"_id": 0})),
            "stock_movements": list(db.stock_movements.find({}, {"_id": 0}))
        }

        with open(BackupUtils.BACKUP_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print(f"Database backup saved to {BackupUtils.BACKUP_FILE}")

    @staticmethod
    def restore_database():

        if not os.path.exists(BackupUtils.BACKUP_FILE):
            print("No backup file found.")
            return

        db = DatabaseConnection().get_database()

        with open(BackupUtils.BACKUP_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        db.products.delete_many({})
        db.sales.delete_many({})
        db.purchases.delete_many({})
        db.stock_movements.delete_many({})

        if data.get("products"):
            db.products.insert_many(data["products"])

        if data.get("sales"):
            db.sales.insert_many(data["sales"])

        if data.get("purchases"):
            db.purchases.insert_many(data["purchases"])

        if data.get("stock_movements"):
            db.stock_movements.insert_many(data["stock_movements"])

        print("Database restored successfully.")