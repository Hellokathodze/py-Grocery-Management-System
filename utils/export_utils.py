import csv
import os


class ExportUtils:

    REPORT_FOLDER = "reports"

    @staticmethod
    def export_inventory(products):

        os.makedirs(ExportUtils.REPORT_FOLDER, exist_ok=True)

        file_path = f"{ExportUtils.REPORT_FOLDER}/inventory_report.csv"

        with open(file_path, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow(
                ["Product ID", "Product Name", "Category", "Price", "Stock"]
            )

            for p in products:
                writer.writerow(
                    [
                        p["product_id"],
                        p["product_name"],
                        p["category"],
                        p["price"],
                        p["stock_quantity"],
                    ]
                )

        print(f"Inventory report exported: {file_path}")

    @staticmethod
    def export_sales(sales):

        os.makedirs(ExportUtils.REPORT_FOLDER, exist_ok=True)

        file_path = f"{ExportUtils.REPORT_FOLDER}/sales_report.csv"

        with open(file_path, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow(
                [
                    "Product ID",
                    "Product Name",
                    "Quantity",
                    "Price",
                    "Total Price",
                    "Date",
                ]
            )

            for s in sales:
                writer.writerow(
                    [
                        s["product_id"],
                        s["product_name"],
                        s["quantity"],
                        s["price"],
                        s["total_price"],
                        s["date"],
                    ]
                )

        print(f"Sales report exported: {file_path}")