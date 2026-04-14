from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox,
    QPushButton, QMessageBox, QSpinBox,
    QFrame, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QHeaderView, QSizePolicy,
    QAbstractItemView
)
from PyQt6.QtCore import Qt
from utils.signal_bus import signal_bus
from datetime import datetime
import os
import subprocess
import platform


class SalesPage(QWidget):

    def __init__(self, sales_controller):
        super().__init__()

        self.sales_controller = sales_controller
        self.inventory_controller = sales_controller.inventory_controller

        self.cart = []
        self.products = []

        # Create bills folder if it doesn't exist
        self.bills_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bills")
        os.makedirs(self.bills_folder, exist_ok=True)

        self.init_ui()

    def init_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # GLOBAL THEME
        self.setStyleSheet("""
            QWidget {
                background-color: #0F172A;
                color: #E2E8F0;
                font-size: 13px;
            }
        """)

        # CARD
        card = QFrame()
        card.setObjectName("billingCard")
        card.setStyleSheet("""
            QFrame#billingCard {
                background-color: #1E293B;
                border-radius: 12px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # ================= TITLE =================
        title = QLabel("🛒 Billing")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "font-size: 22px; font-weight: bold; "
            "background-color: transparent; border: none;"
        )
        layout.addWidget(title)

        # ================= PRODUCT + QTY ROW =================
        row = QHBoxLayout()
        row.setSpacing(10)

        self.product_dropdown = QComboBox()
        self.product_dropdown.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.product_dropdown.setMinimumHeight(38)
        self.product_dropdown.setStyleSheet(self.dropdown_style())
        row.addWidget(self.product_dropdown, 3)

        self.quantity = QSpinBox()
        self.quantity.setMinimum(1)
        self.quantity.setMaximum(10000)
        self.quantity.setMinimumHeight(38)
        self.quantity.setStyleSheet(self.spinbox_style())
        row.addWidget(self.quantity, 1)

        layout.addLayout(row)

        # ================= STOCK =================
        self.stock_label = QLabel("Stock: 0")
        self.stock_label.setStyleSheet(
            "color: #94A3B8; font-size: 12px; "
            "background-color: transparent; border: none;"
        )
        layout.addWidget(self.stock_label)

        # ================= BUTTONS ROW =================
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        add_btn = self.create_button("➕ Add to Cart", "#22C55E")
        add_btn.clicked.connect(self.add_to_cart)

        remove_btn = self.create_button("❌ Remove", "#EF4444")
        remove_btn.clicked.connect(self.remove_item)

        btn_row.addWidget(add_btn)
        btn_row.addWidget(remove_btn)

        layout.addLayout(btn_row)

        # ================= TABLE SECTION =================
        table_label = QLabel("📋 Cart Items")
        table_label.setStyleSheet(
            "font-size: 14px; font-weight: bold; color: #CBD5E1; "
            "padding-top: 6px; background-color: transparent; border: none;"
        )
        layout.addWidget(table_label)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Product", "Qty", "Price (₹)", "Total (₹)"]
        )

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setStretchLastSection(True)
        header.setMinimumHeight(38)
        header.setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        self.table.verticalHeader().setDefaultSectionSize(36)
        self.table.verticalHeader().setVisible(False)

        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.table.setMinimumHeight(180)
        self.table.setMaximumHeight(300)
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.table.setStyleSheet(self.table_style())

        layout.addWidget(self.table, 1)

        # ================= TOTAL =================
        total_frame = QFrame()
        total_frame.setObjectName("totalFrame")
        total_frame.setStyleSheet("""
            QFrame#totalFrame {
                background-color: #273449;
                border-radius: 8px;
            }
        """)
        total_layout = QHBoxLayout()
        total_layout.setContentsMargins(14, 10, 14, 10)

        total_text = QLabel("Grand Total (incl. 18% GST):")
        total_text.setStyleSheet(
            "font-size: 14px; color: #94A3B8; "
            "background-color: transparent; border: none;"
        )

        self.total_label = QLabel("₹0.00")
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.total_label.setStyleSheet(
            "font-size: 22px; font-weight: bold; color: #22C55E; "
            "background-color: transparent; border: none;"
        )

        total_layout.addWidget(total_text)
        total_layout.addWidget(self.total_label)
        total_frame.setLayout(total_layout)

        layout.addWidget(total_frame)

        # ================= CHECKOUT BUTTON =================
        checkout_btn = self.create_button("🧾 Checkout", "#3B82F6")
        checkout_btn.setMinimumHeight(44)
        checkout_btn.clicked.connect(self.checkout)
        layout.addWidget(checkout_btn)

        card.setLayout(layout)
        main_layout.addWidget(card)

        self.setLayout(main_layout)

        # Listen for inventory changes from ANY page
        signal_bus.inventory_updated.connect(self.load_products)

        self.load_products()

    # ================= STYLES =================
    def dropdown_style(self):
        return """
            QComboBox {
                background-color: #334155;
                border-radius: 8px;
                padding: 8px 12px;
                border: 1px solid #475569;
                color: white;
                font-size: 13px;
            }
            QComboBox:hover {
                border: 1px solid #3B82F6;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: #334155;
                color: white;
                selection-background-color: #3B82F6;
                border: 1px solid #475569;
                border-radius: 4px;
                padding: 4px;
            }
        """

    def spinbox_style(self):
        return """
            QSpinBox {
                background-color: #334155;
                border-radius: 8px;
                padding: 8px 12px;
                border: 1px solid #475569;
                color: white;
                font-size: 13px;
            }
            QSpinBox:hover {
                border: 1px solid #3B82F6;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #475569;
                border: none;
                width: 20px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #3B82F6;
            }
        """

    def table_style(self):
        return """
            QTableWidget {
                background-color: #1E293B;
                color: #E2E8F0;
                border: 1px solid #334155;
                border-radius: 8px;
                font-size: 13px;
                gridline-color: transparent;
            }

            QHeaderView::section {
                background-color: #334155;
                color: #F1F5F9;
                padding: 8px 12px;
                border: none;
                font-weight: bold;
                font-size: 13px;
                min-height: 22px;
            }

            QTableWidget::item {
                padding: 6px 10px;
                border-bottom: 1px solid #293548;
            }

            QTableWidget::item:selected {
                background-color: #3B82F6;
                color: #FFFFFF;
            }

            QTableWidget::item:alternate {
                background-color: #1a2f4a;
            }

            QScrollBar:vertical {
                background-color: #1E293B;
                width: 8px;
                border-radius: 4px;
                margin: 0px;
            }

            QScrollBar::handle:vertical {
                background-color: #475569;
                border-radius: 4px;
                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover {
                background-color: #64748B;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical,
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
                border: none;
            }
        """

    def create_button(self, text, color):
        btn = QPushButton(text)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumHeight(40)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                padding: 10px 16px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 13px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {color}CC;
            }}
            QPushButton:pressed {{
                background-color: {color}AA;
            }}
        """)
        return btn

    # ================= LOAD PRODUCTS =================
    def load_products(self):

        self.products = self.inventory_controller.get_all_products()
        self.product_dropdown.clear()

        for p in self.products:
            self.product_dropdown.addItem(
                f"{p['product_id']} - {p['product_name']}"
            )

        try:
            self.product_dropdown.currentIndexChanged.disconnect(self.update_stock)
        except TypeError:
            pass

        self.product_dropdown.currentIndexChanged.connect(self.update_stock)
        self.update_stock()

    # ================= STOCK DISPLAY =================
    def update_stock(self):

        index = self.product_dropdown.currentIndex()

        if index < 0 or index >= len(self.products):
            self.stock_label.setText("Stock: 0")
            return

        product = self.products[index]
        stock = product.get("stock_quantity", 0)

        if stock <= 5:
            self.stock_label.setText(f"⚠️ Stock: {stock} (Low)")
            self.stock_label.setStyleSheet(
                "color: #F59E0B; font-size: 12px; "
                "background-color: transparent; border: none;"
            )
        else:
            self.stock_label.setText(f"Stock: {stock}")
            self.stock_label.setStyleSheet(
                "color: #94A3B8; font-size: 12px; "
                "background-color: transparent; border: none;"
            )

    # ================= ADD TO CART =================
    def add_to_cart(self):

        index = self.product_dropdown.currentIndex()

        if index < 0:
            return

        product = self.products[index]
        qty = self.quantity.value()
        stock = product.get("stock_quantity", 0)

        if qty > stock:
            QMessageBox.warning(self, "Error", "Not enough stock!")
            return

        for item in self.cart:
            if item["product_id"] == product["product_id"]:
                if item["qty"] + qty > stock:
                    QMessageBox.warning(self, "Error", "Not enough stock!")
                    return
                item["qty"] += qty
                item["total"] = item["qty"] * item["price"]
                self.update_table()
                return

        self.cart.append({
            "product_id": product["product_id"],
            "name": product["product_name"],
            "qty": qty,
            "price": product["price"],
            "total": qty * product["price"]
        })

        self.update_table()

    # ================= REMOVE ITEM =================
    def remove_item(self):

        row = self.table.currentRow()

        if row >= 0:
            self.cart.pop(row)
            self.update_table()
        else:
            QMessageBox.warning(self, "Error", "Select a row to remove!")

    # ================= UPDATE TABLE =================
    def update_table(self):

        self.table.setRowCount(len(self.cart))
        total_bill = 0

        for row, item in enumerate(self.cart):

            name_item = QTableWidgetItem(item["name"])
            qty_item = QTableWidgetItem(str(item["qty"]))
            price_item = QTableWidgetItem(f"₹{item['price']:,.2f}")
            total_item = QTableWidgetItem(f"₹{item['total']:,.2f}")

            qty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            total_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.table.setItem(row, 0, name_item)
            self.table.setItem(row, 1, qty_item)
            self.table.setItem(row, 2, price_item)
            self.table.setItem(row, 3, total_item)

            total_bill += item["total"]

        self.total_label.setText(f"₹{total_bill:,.2f}")

    # ================= CHECKOUT =================
    def checkout(self):

        if not self.cart:
            QMessageBox.warning(self, "Error", "Cart is empty!")
            return

        success = self.sales_controller.record_bulk_sale(self.cart)

        if not success:
            QMessageBox.warning(self, "Error", "Sale failed due to stock issue!")
            return

        bill_path = self.generate_pdf_bill()

        self.cart.clear()
        self.table.setRowCount(0)
        self.total_label.setText("₹0.00")

        self.load_products()
        signal_bus.inventory_updated.emit()

        if bill_path:
            reply = QMessageBox.information(
                self, "Sale Complete",
                f"Sale completed!\n\nBill saved to:\n{bill_path}\n\nOpen the bill?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.open_file(bill_path)
        else:
            QMessageBox.information(self, "Success", "Sale completed!")

    # ================= PDF BILL GENERATION =================
    def generate_pdf_bill(self):

        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.units import mm
            from reportlab.lib import colors
            from reportlab.pdfgen import canvas

            now = datetime.now()
            bill_number = now.strftime("BILL-%Y%m%d-%H%M%S")
            bill_date = now.strftime("%d/%m/%Y  %I:%M %p")
            filename = f"{bill_number}.pdf"
            filepath = os.path.join(self.bills_folder, filename)

            width, height = A4
            c = canvas.Canvas(filepath, pagesize=A4)

            # ===== HEADER =====
            c.setFillColor(colors.HexColor("#1E293B"))
            c.rect(0, height - 100, width, 100, fill=True, stroke=False)

            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 22)
            c.drawString(30, height - 45, "KailashGeneralStore")

            c.setFont("Helvetica", 10)
            c.setFillColor(colors.HexColor("#94A3B8"))
            c.drawString(30, height - 65, "Your trusted grocery partner")
            c.drawString(30, height - 80, "GSTIN: 27ABCDE1234F1Z5")

            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 12)
            c.drawRightString(width - 30, height - 40, "TAX INVOICE")

            c.setFont("Helvetica", 10)
            c.setFillColor(colors.HexColor("#94A3B8"))
            c.drawRightString(width - 30, height - 58, f"#{bill_number}")
            c.drawRightString(width - 30, height - 74, bill_date)

            # ===== BILL INFO BAR =====
            y = height - 130

            c.setFillColor(colors.HexColor("#F1F5F9"))
            c.rect(30, y - 5, width - 60, 25, fill=True, stroke=False)

            c.setFillColor(colors.HexColor("#334155"))
            c.setFont("Helvetica-Bold", 9)
            c.drawString(40, y + 2, f"Bill No: {bill_number}")
            c.drawString(250, y + 2, f"Date: {bill_date}")
            c.drawRightString(width - 40, y + 2, f"Items: {len(self.cart)}")

            # ===== TABLE HEADER =====
            y -= 40

            c.setFillColor(colors.HexColor("#1E293B"))
            c.rect(30, y - 5, width - 60, 25, fill=True, stroke=False)

            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(40, y + 2, "#")
            c.drawString(65, y + 2, "Product")
            c.drawRightString(310, y + 2, "Price")
            c.drawRightString(370, y + 2, "Qty")
            c.drawRightString(450, y + 2, "Taxable Amt")
            c.drawRightString(width - 40, y + 2, "Total")

            # ===== TABLE ROWS =====
            y -= 10
            subtotal = 0

            c.setFont("Helvetica", 10)

            for i, item in enumerate(self.cart):
                y -= 25

                if i % 2 == 0:
                    c.setFillColor(colors.HexColor("#F8FAFC"))
                    c.rect(30, y - 5, width - 60, 25, fill=True, stroke=False)

                item_total = item["total"]
                # Price is inclusive of GST, so taxable amount = total / 1.18
                taxable_amount = round(item_total / 1.18, 2)

                c.setFillColor(colors.HexColor("#1E293B"))
                c.drawString(40, y + 2, str(i + 1))
                c.drawString(65, y + 2, item["name"])
                c.drawRightString(310, y + 2, f"Rs.{item['price']:,.2f}")
                c.drawRightString(370, y + 2, str(item["qty"]))
                c.drawRightString(450, y + 2, f"Rs.{taxable_amount:,.2f}")

                c.setFont("Helvetica-Bold", 10)
                c.drawRightString(width - 40, y + 2, f"Rs.{item_total:,.2f}")
                c.setFont("Helvetica", 10)

                subtotal += item_total

            # ===== SEPARATOR =====
            y -= 15
            c.setStrokeColor(colors.HexColor("#CBD5E1"))
            c.setLineWidth(1)
            c.line(30, y, width - 30, y)

            # ===== TAX CALCULATION =====
            # Prices are MRP (inclusive of 18% GST)
            # Taxable value = Total / 1.18
            # GST = Total - Taxable value
            # CGST = GST / 2 (9%)
            # SGST = GST / 2 (9%)

            taxable_total = round(subtotal / 1.18, 2)
            total_gst = round(subtotal - taxable_total, 2)
            cgst = round(total_gst / 2, 2)
            sgst = round(total_gst / 2, 2)

            # ===== SUBTOTAL / TAX / TOTAL SECTION =====
            y -= 25

            c.setFillColor(colors.HexColor("#64748B"))
            c.setFont("Helvetica", 11)
            c.drawString(280, y, "Taxable Amount:")
            c.setFillColor(colors.HexColor("#1E293B"))
            c.drawRightString(width - 40, y, f"Rs.{taxable_total:,.2f}")

            y -= 22
            c.setFillColor(colors.HexColor("#64748B"))
            c.drawString(280, y, "CGST (9%):")
            c.setFillColor(colors.HexColor("#1E293B"))
            c.drawRightString(width - 40, y, f"Rs.{cgst:,.2f}")

            y -= 22
            c.setFillColor(colors.HexColor("#64748B"))
            c.drawString(280, y, "SGST (9%):")
            c.setFillColor(colors.HexColor("#1E293B"))
            c.drawRightString(width - 40, y, f"Rs.{sgst:,.2f}")

            y -= 10
            c.setStrokeColor(colors.HexColor("#CBD5E1"))
            c.setLineWidth(0.5)
            c.line(280, y, width - 30, y)

            y -= 22
            c.setFillColor(colors.HexColor("#64748B"))
            c.setFont("Helvetica-Bold", 11)
            c.drawString(280, y, "Total GST (18%):")
            c.setFillColor(colors.HexColor("#1E293B"))
            c.drawRightString(width - 40, y, f"Rs.{total_gst:,.2f}")

            # ===== GRAND TOTAL BOX =====
            y -= 35
            c.setFillColor(colors.HexColor("#1E293B"))
            c.rect(260, y - 10, width - 290, 35, fill=True, stroke=False)

            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 14)
            c.drawString(275, y + 2, "GRAND TOTAL")
            c.drawRightString(width - 40, y + 2, f"Rs.{subtotal:,.2f}")

            # ===== AMOUNT IN WORDS (optional nice touch) =====
            y -= 30
            c.setFillColor(colors.HexColor("#64748B"))
            c.setFont("Helvetica-Oblique", 9)
            c.drawString(30, y, f"Amount inclusive of GST @ 18%")

            # ===== FOOTER =====
            footer_y = 60

            c.setStrokeColor(colors.HexColor("#E2E8F0"))
            c.setLineWidth(0.5)
            c.line(30, footer_y + 20, width - 30, footer_y + 20)

            c.setFillColor(colors.HexColor("#94A3B8"))
            c.setFont("Helvetica", 9)
            c.drawCentredString(width / 2, footer_y, "Thank you for shopping with us!")
            c.drawCentredString(width / 2, footer_y - 14,
                                "KailashGeneralStore  |  GSTIN: 27ABCDE1234F1Z5  |  Contact: +91 9619781254")

            c.save()

            print(f"\n✅ Bill saved: {filepath}")
            return filepath

        except ImportError:
            print("\n⚠️ reportlab not installed. Run: pip install reportlab")
            QMessageBox.warning(
                self, "Missing Library",
                "PDF generation requires 'reportlab'.\n\n"
                "Install it with:\n  pip install reportlab"
            )
            return None

        except Exception as e:
            print(f"\n❌ Bill generation error: {e}")
            QMessageBox.warning(self, "Error", f"Bill generation failed:\n{e}")
            return None

    # ================= OPEN FILE =================
    def open_file(self, filepath):

        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(filepath)
            elif system == "Darwin":
                subprocess.Popen(["open", filepath])
            else:
                subprocess.Popen(["xdg-open", filepath])
        except Exception as e:
            print(f"Could not open file: {e}")