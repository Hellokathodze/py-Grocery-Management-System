from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QLineEdit, QFrame, QHeaderView,
    QSizePolicy, QAbstractItemView, QHBoxLayout,
    QScrollArea
)
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt
from utils.signal_bus import signal_bus
from datetime import datetime


class InventoryPage(QWidget):

    def __init__(self, inventory_controller):
        super().__init__()
        self.inventory_controller = inventory_controller

        signal_bus.inventory_updated.connect(self.load_products)

        self.init_ui()

    def init_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(12)

        # GLOBAL THEME
        self.setStyleSheet("""
            QWidget {
                background-color: #0F172A;
                color: #E2E8F0;
                font-size: 13px;
            }
        """)

        # ================= EXPIRY ALERT BANNER =================
        self.expiry_alert_frame = self.create_alert_banner(
            object_name="expiryAlert",
            bg_color="#451A1A",
            border_color="#7F1D1D",
            title_text="Expiry Alerts",
            title_color="#FCA5A5",
            badge_bg="#FCA5A5",
            icon="⚠️",
            scroll_handle_color="#7F1D1D"
        )
        main_layout.addWidget(self.expiry_alert_frame["frame"])

        # ================= REORDER ALERT BANNER =================
        self.reorder_alert_frame = self.create_alert_banner(
            object_name="reorderAlert",
            bg_color="#1A3045",
            border_color="#1E4976",
            title_text="Low Stock Alerts",
            title_color="#93C5FD",
            badge_bg="#3B82F6",
            icon="📦",
            scroll_handle_color="#1E4976"
        )
        main_layout.addWidget(self.reorder_alert_frame["frame"])

        # ================= MAIN CARD =================
        card = QFrame()
        card.setObjectName("inventoryCard")
        card.setStyleSheet("""
            QFrame#inventoryCard {
                background-color: #1E293B;
                border-radius: 12px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # TITLE
        title = QLabel("📦 Inventory Management")
        title.setStyleSheet(
            "font-size: 22px; font-weight: bold; color: #F1F5F9; "
            "background: transparent; border: none;"
        )
        layout.addWidget(title)

        # SEARCH
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search product...")
        self.search_input.setMinimumHeight(40)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #0F172A;
                border-radius: 10px;
                padding: 8px 14px;
                border: 1.5px solid #2A3A55;
                color: white;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1.5px solid #3B82F6;
                background-color: #111E36;
            }
            QLineEdit:hover {
                border: 1.5px solid #3B6ECF;
            }
        """)
        self.search_input.textChanged.connect(self.search_products)
        layout.addWidget(self.search_input)

        # TABLE — 7 columns
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Product Name", "Price (₹)", "Stock Level",
             "Stock Status", "Expiry Date", "Expiry Status"]
        )

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setStretchLastSection(True)
        header.setMinimumHeight(40)
        header.setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        self.table.verticalHeader().setDefaultSectionSize(40)
        self.table.verticalHeader().setVisible(False)

        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.table.setMinimumHeight(300)

        self.table.setStyleSheet(self.table_style())

        layout.addWidget(self.table)

        card.setLayout(layout)
        main_layout.addWidget(card)

        self.setLayout(main_layout)

        self.load_products()

    # ================= REUSABLE ALERT BANNER FACTORY =================
    def create_alert_banner(self, object_name, bg_color, border_color,
                            title_text, title_color, badge_bg, icon,
                            scroll_handle_color):

        frame = QFrame()
        frame.setObjectName(object_name)
        frame.setStyleSheet(f"""
            QFrame#{object_name} {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 10px;
            }}
        """)

        alert_layout = QVBoxLayout()
        alert_layout.setContentsMargins(16, 12, 16, 12)
        alert_layout.setSpacing(6)

        # Title row
        title_row = QHBoxLayout()

        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 18px; background: transparent; border: none;")

        title_label = QLabel(title_text)
        title_label.setStyleSheet(
            f"font-size: 15px; font-weight: bold; color: {title_color}; "
            "background: transparent; border: none;"
        )

        title_row.addWidget(icon_label)
        title_row.addWidget(title_label)
        title_row.addStretch()

        count_label = QLabel("")
        count_label.setStyleSheet(
            f"font-size: 11px; font-weight: bold; color: #1E293B; "
            f"background-color: {badge_bg}; border-radius: 8px; "
            "padding: 2px 8px;"
        )
        title_row.addWidget(count_label)

        alert_layout.addLayout(title_row)

        # Scrollable items area
        items_container = QWidget()
        items_container.setStyleSheet("background: transparent; border: none;")
        items_layout = QVBoxLayout()
        items_layout.setContentsMargins(0, 0, 0, 0)
        items_layout.setSpacing(4)
        items_container.setLayout(items_layout)

        scroll = QScrollArea()
        scroll.setObjectName(f"{object_name}Scroll")
        scroll.setWidgetResizable(True)
        scroll.setMaximumHeight(100)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(f"""
            QScrollArea#{object_name}Scroll {{
                background: transparent;
                border: none;
            }}
            QScrollBar:vertical {{
                background-color: {bg_color};
                width: 6px;
                border-radius: 3px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {scroll_handle_color};
                border-radius: 3px;
                min-height: 20px;
            }}
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical,
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {{
                background: none;
                border: none;
            }}
        """)
        scroll.setWidget(items_container)

        alert_layout.addWidget(scroll)
        frame.setLayout(alert_layout)

        # Hidden by default
        frame.hide()

        return {
            "frame": frame,
            "count_label": count_label,
            "items_layout": items_layout
        }

    # ================= LOAD =================
    def load_products(self):
        self.table.setRowCount(0)
        self.search_products()

    # ================= SEARCH =================
    def search_products(self):

        keyword = self.search_input.text().strip()

        if keyword:
            products = self.inventory_controller.search_product(keyword)
            all_with_expiry = self.inventory_controller.get_products_with_expiry_status()
            expiry_map = {p.get("product_id"): p for p in all_with_expiry}

            enriched = []
            for p in products:
                pid = p.get("product_id")
                if pid in expiry_map:
                    enriched.append(expiry_map[pid])
                else:
                    p["expiry_status"] = "no_date"
                    p["days_remaining"] = None
                    enriched.append(p)
            products = enriched
        else:
            products = self.inventory_controller.get_products_with_expiry_status()

        self.populate_table(products)
        self.update_expiry_alerts(products)
        self.update_reorder_alerts(products)

    # ================= EXPIRY ALERTS =================
    def update_expiry_alerts(self, products):

        items_layout = self.expiry_alert_frame["items_layout"]
        count_label = self.expiry_alert_frame["count_label"]
        frame = self.expiry_alert_frame["frame"]

        # Clear old
        while items_layout.count():
            child = items_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        alert_products = [
            p for p in products
            if p.get("expiry_status") in ("expired", "expiring_soon")
        ]

        if not alert_products:
            frame.hide()
            return

        frame.show()
        count_label.setText(f"{len(alert_products)} alert(s)")

        for p in alert_products:
            name = p.get("product_name", "Unknown")
            expiry_date = p.get("expiry_date", "N/A")
            days = p.get("days_remaining", 0)
            status = p.get("expiry_status", "")

            if status == "expired":
                msg = f"🔴  {name}  —  Expired on {expiry_date}  ({abs(days)} days ago)"
                text_color = "#FCA5A5"
            else:
                msg = f"🟡  {name}  —  Expires on {expiry_date}  ({days} day(s) left)"
                text_color = "#FDE68A"

            label = QLabel(msg)
            label.setStyleSheet(
                f"font-size: 12px; color: {text_color}; "
                "background: transparent; border: none; padding: 2px 0;"
            )
            items_layout.addWidget(label)

    # ================= REORDER ALERTS =================
    def update_reorder_alerts(self, products):

        items_layout = self.reorder_alert_frame["items_layout"]
        count_label = self.reorder_alert_frame["count_label"]
        frame = self.reorder_alert_frame["frame"]

        # Clear old
        while items_layout.count():
            child = items_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        low_stock_products = []
        for p in products:
            stock = p.get("stock_quantity", 0)
            reorder = p.get("reorder_level", 0)

            if reorder > 0 and stock <= reorder:
                low_stock_products.append(p)

        if not low_stock_products:
            frame.hide()
            return

        frame.show()
        count_label.setText(f"{len(low_stock_products)} alert(s)")

        for p in low_stock_products:
            name = p.get("product_name", "Unknown")
            stock = p.get("stock_quantity", 0)
            reorder = p.get("reorder_level", 0)

            if stock == 0:
                msg = f"🔴  {name}  —  Out of stock!  (Reorder level: {reorder})"
                text_color = "#FCA5A5"
            else:
                msg = f"🟠  {name}  —  Stock: {stock}  (Reorder level: {reorder}, need {reorder - stock} more)"
                text_color = "#FDBA74"

            label = QLabel(msg)
            label.setStyleSheet(
                f"font-size: 12px; color: {text_color}; "
                "background: transparent; border: none; padding: 2px 0;"
            )
            items_layout.addWidget(label)

    # ================= TABLE =================
    def populate_table(self, products):

        self.table.setRowCount(len(products))

        for row, p in enumerate(products):

            stock = p.get("stock_quantity", 0)
            price = p.get("price", 0)
            reorder = p.get("reorder_level", 0)
            expiry_date = p.get("expiry_date", "")
            expiry_status = p.get("expiry_status", "no_date")
            days_remaining = p.get("days_remaining", None)

            id_item = QTableWidgetItem(str(p.get("product_id", "")))
            name_item = QTableWidgetItem(p.get("product_name", ""))
            price_item = QTableWidgetItem(f"₹{price:,.2f}")
            stock_item = QTableWidgetItem(str(stock))

            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            stock_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.table.setItem(row, 0, id_item)
            self.table.setItem(row, 1, name_item)
            self.table.setItem(row, 2, price_item)
            self.table.setItem(row, 3, stock_item)

            # Stock status — now considers reorder level
            if stock == 0:
                stock_text = "● Out of Stock"
                stock_color = "#EF4444"
            elif reorder > 0 and stock <= reorder:
                stock_text = f"● Low ({stock}/{reorder})"
                stock_color = "#F59E0B"
            else:
                stock_text = "● In Stock"
                stock_color = "#22C55E"

            stock_status_item = QTableWidgetItem(stock_text)
            stock_status_item.setForeground(QColor(stock_color))
            stock_status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 4, stock_status_item)

            # Expiry date column
            expiry_date_item = QTableWidgetItem(str(expiry_date) if expiry_date else "N/A")
            expiry_date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            if expiry_status == "expired":
                expiry_date_item.setForeground(QColor("#EF4444"))
            elif expiry_status == "expiring_soon":
                expiry_date_item.setForeground(QColor("#F59E0B"))
            else:
                expiry_date_item.setForeground(QColor("#94A3B8"))

            self.table.setItem(row, 5, expiry_date_item)

            # Expiry status column
            if expiry_status == "expired":
                expiry_text = f"🔴 Expired ({abs(days_remaining)}d ago)"
                expiry_color = "#EF4444"
            elif expiry_status == "expiring_soon":
                expiry_text = f"🟡 {days_remaining}d left"
                expiry_color = "#F59E0B"
            elif expiry_status == "ok":
                expiry_text = f"🟢 {days_remaining}d left"
                expiry_color = "#22C55E"
            else:
                expiry_text = "—"
                expiry_color = "#475569"

            expiry_status_item = QTableWidgetItem(expiry_text)
            expiry_status_item.setForeground(QColor(expiry_color))
            expiry_status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 6, expiry_status_item)

            # Highlight expired rows
            if expiry_status == "expired":
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    if item:
                        item.setBackground(QColor("#2D1515"))

    # ================= STYLE =================
    def table_style(self):
        return """
            QTableWidget {
                background-color: #1E293B;
                color: #E2E8F0;
                border: 1px solid #2A3A55;
                border-radius: 8px;
                font-size: 13px;
                gridline-color: transparent;
            }

            QHeaderView::section {
                background-color: #273449;
                color: #F1F5F9;
                padding: 8px 10px;
                border: none;
                font-weight: bold;
                font-size: 12px;
                min-height: 22px;
            }

            QTableWidget::item {
                padding: 6px 8px;
                border-bottom: 1px solid #253045;
            }

            QTableWidget::item:selected {
                background-color: #3B82F6;
                color: #FFFFFF;
            }

            QTableWidget::item:alternate {
                background-color: #1a2d44;
            }

            QScrollBar:vertical {
                background-color: #1E293B;
                width: 8px;
                border-radius: 4px;
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

            QScrollBar:horizontal {
                background-color: #1E293B;
                height: 8px;
                border-radius: 4px;
            }

            QScrollBar::handle:horizontal {
                background-color: #475569;
                border-radius: 4px;
                min-width: 30px;
            }

            QScrollBar::handle:horizontal:hover {
                background-color: #64748B;
            }

            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal,
            QScrollBar::add-page:horizontal,
            QScrollBar::sub-page:horizontal {
                background: none;
                border: none;
            }
        """