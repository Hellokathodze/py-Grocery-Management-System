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
                        p.get("product_id", ""),
                        p.get("product_name", ""),
                        p.get("category", ""),
                        p.get("price", ""),
                        p.get("stock_quantity", "")
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
                    "Day",
                    "Month",
                    "Season"
                ]
            )

            for s in sales:

                writer.writerow(
                    [
                        s.get("product_id", ""),
                        s.get("product_name", ""),
                        s.get("quantity", ""),
                        s.get("price", ""),
                        s.get("total_price", ""),
                        s.get("date", ""),
                        s.get("day_of_week", ""),
                        s.get("month", ""),
                        s.get("season", "")
                    ]
                )

        print(f"Sales report exported: {file_path}")