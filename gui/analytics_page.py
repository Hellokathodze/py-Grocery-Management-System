from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QHBoxLayout, QFrame, QTableWidget,
    QTableWidgetItem, QHeaderView, QSizePolicy,
    QScrollArea, QGraphicsDropShadowEffect,
    QGraphicsOpacityEffect
)
from PyQt6.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve,
    QPoint, QSize
)
from PyQt6.QtGui import QColor, QFont

import matplotlib
matplotlib.use("QtAgg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import patheffects
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict


# ============================================================
#  ANIMATED STAT CARD — counts up on load + hover glow
# ============================================================
class AnimatedCard(QFrame):

    def __init__(self, title, default_value, accent, icon, parent=None):
        super().__init__(parent)

        self.accent = accent
        self._target_value = 0
        self._current_value = 0
        self._is_currency = False
        self._hovered = False

        self.setObjectName("statCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._apply_style(hovered=False)

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(4)

        top_row = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(
            "font-size: 20px; background: transparent; border: none;"
        )
        title_label = QLabel(title)
        title_label.setStyleSheet(
            "font-size: 11px; color: #64748B; font-weight: bold; "
            "letter-spacing: 0.8px; background: transparent; border: none;"
        )
        top_row.addWidget(icon_label)
        top_row.addWidget(title_label)
        top_row.addStretch()
        layout.addLayout(top_row)

        self.value_label = QLabel(default_value)
        self.value_label.setStyleSheet(
            f"font-size: 24px; font-weight: bold; color: {accent}; "
            "background: transparent; border: none; padding-left: 2px;"
        )
        layout.addWidget(self.value_label)

        self.setLayout(layout)

        # Animation timer
        self._anim_timer = QTimer()
        self._anim_timer.setInterval(18)
        self._anim_timer.timeout.connect(self._tick_counter)

    def _apply_style(self, hovered=False):
        border_w = "4px" if hovered else "3px"
        bg_start = "#253350" if hovered else "#1E293B"
        bg_end = "#1E2C45" if hovered else "#172033"
        self.setStyleSheet(f"""
            QFrame#statCard {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 {bg_start}, stop:1 {bg_end}
                );
                border-radius: 12px;
                border-bottom: {border_w} solid {self.accent};
            }}
        """)

    def enterEvent(self, event):
        self._hovered = True
        self._apply_style(hovered=True)
        # Add glow shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(self.accent))
        self.setGraphicsEffect(shadow)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self._apply_style(hovered=False)
        self.setGraphicsEffect(None)
        super().leaveEvent(event)

    def animate_to(self, value, is_currency=False):
        self._target_value = value
        self._current_value = 0
        self._is_currency = is_currency
        self._anim_timer.start()

    def _tick_counter(self):
        step = max(1, int(self._target_value / 30))
        self._current_value = min(self._current_value + step, self._target_value)

        if self._is_currency:
            self.value_label.setText(f"₹{self._current_value:,.2f}")
        else:
            self.value_label.setText(str(self._current_value))

        if self._current_value >= self._target_value:
            self._anim_timer.stop()


# ============================================================
#  HOVER TOOLTIP for charts
# ============================================================
class ChartTooltip(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QLabel {
                background-color: #1A2742;
                color: #F1F5F9;
                border: 1px solid #3B82F6;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 12px;
                font-weight: bold;
            }
        """)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hide()

    def show_at(self, text, global_pos, parent_widget):
        self.setText(text)
        self.adjustSize()
        # Convert global position to parent-relative
        local = parent_widget.mapFromGlobal(global_pos)
        x = local.x() - self.width() // 2
        y = local.y() - self.height() - 12
        # Clamp inside parent
        x = max(4, min(x, parent_widget.width() - self.width() - 4))
        y = max(4, y)
        self.move(x, y)
        self.show()
        self.raise_()


# ============================================================
#  MAIN ANALYTICS PAGE
# ============================================================
class AnalyticsPage(QWidget):

    def __init__(self, inventory_controller, sales_controller):
        super().__init__()

        self.inventory_controller = inventory_controller
        self.sales_controller = sales_controller

        # Store chart data for hover lookups
        self._bar_data = {}
        self._donut_data = {}
        self._line_data = {}

        # Store original bar colors/donut offsets for reset
        self._bar_original_colors = []
        self._donut_original_offsets = []

        self.init_ui()

    def init_ui(self):

        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setObjectName("pageScroll")
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(self.scroll_style())

        container = QWidget()
        container.setStyleSheet("background-color: #0F172A; border: none;")

        main_layout = QVBoxLayout()
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(15, 15, 15, 15)

        self.setStyleSheet("""
            QWidget {
                background-color: #0F172A;
                color: #E2E8F0;
                font-size: 13px;
            }
        """)

        # ================= TITLE =================
        title_row = QHBoxLayout()
        title = QLabel("📊 Analytics Dashboard")
        title.setStyleSheet(
            "font-size: 22px; font-weight: bold; color: #F1F5F9; "
            "background: transparent; border: none;"
        )
        title_row.addWidget(title)
        title_row.addStretch()

        # Refresh button
        from PyQt6.QtWidgets import QPushButton
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #1E293B;
                color: #94A3B8;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 6px 14px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #273449;
                color: #E2E8F0;
                border: 1px solid #3B82F6;
            }
        """)
        refresh_btn.clicked.connect(self.load_data)
        title_row.addWidget(refresh_btn)

        main_layout.addLayout(title_row)

        # ================= STAT CARDS =================
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(12)

        self.products_card = AnimatedCard("Total Products", "0", "#3B82F6", "📦")
        self.revenue_card = AnimatedCard("Total Revenue", "₹0", "#10B981", "💰")
        self.transactions_card = AnimatedCard("Transactions", "0", "#F59E0B", "🧾")
        self.today_card = AnimatedCard("Today Revenue", "₹0", "#8B5CF6", "📅")

        cards_layout.addWidget(self.products_card)
        cards_layout.addWidget(self.revenue_card)
        cards_layout.addWidget(self.transactions_card)
        cards_layout.addWidget(self.today_card)

        main_layout.addLayout(cards_layout)

        # ================= CHARTS ROW 1 =================
        charts_row1 = QHBoxLayout()
        charts_row1.setSpacing(12)

        # Bar chart
        bar_card = self.create_chart_frame("📈 Revenue by Product")
        bar_layout = bar_card.layout()

        self.bar_canvas = FigureCanvas(plt.Figure(figsize=(5, 3.2), dpi=100))
        self.bar_canvas.setStyleSheet("background-color: #1E293B; border: none;")
        self.bar_canvas.setMinimumHeight(280)
        bar_layout.addWidget(self.bar_canvas)

        self.bar_tooltip = ChartTooltip(self.bar_canvas)

        # Donut chart
        donut_card = self.create_chart_frame("🍩 Sales by Category")
        donut_layout = donut_card.layout()

        self.donut_canvas = FigureCanvas(plt.Figure(figsize=(3.5, 3.2), dpi=100))
        self.donut_canvas.setStyleSheet("background-color: #1E293B; border: none;")
        self.donut_canvas.setMinimumHeight(280)
        donut_layout.addWidget(self.donut_canvas)

        self.donut_tooltip = ChartTooltip(self.donut_canvas)

        charts_row1.addWidget(bar_card, 3)
        charts_row1.addWidget(donut_card, 2)

        main_layout.addLayout(charts_row1)

        # ================= AREA CHART =================
        area_card = self.create_chart_frame("📉 Revenue Trend (Last 7 Days)")
        area_layout = area_card.layout()

        self.area_canvas = FigureCanvas(plt.Figure(figsize=(8, 2.8), dpi=100))
        self.area_canvas.setStyleSheet("background-color: #1E293B; border: none;")
        self.area_canvas.setMinimumHeight(250)
        area_layout.addWidget(self.area_canvas)

        self.line_tooltip = ChartTooltip(self.area_canvas)

        main_layout.addWidget(area_card)

        # ================= TABLE =================
        table_card = QFrame()
        table_card.setObjectName("tableCard")
        table_card.setStyleSheet("""
            QFrame#tableCard {
                background-color: #1E293B;
                border-radius: 12px;
            }
        """)
        tbl_layout = QVBoxLayout()
        tbl_layout.setContentsMargins(14, 14, 14, 14)
        tbl_layout.setSpacing(6)

        table_title = QLabel("📋 Recent Transactions")
        table_title.setStyleSheet(
            "font-size: 15px; font-weight: bold; color: #E2E8F0; "
            "padding: 2px 0px 8px 2px; background-color: transparent; border: none;"
        )
        tbl_layout.addWidget(table_title)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Product", "Qty", "Total (₹)", "Date"])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setStretchLastSection(True)
        header.setMinimumHeight(36)

        self.table.setMinimumHeight(220)
        self.table.setMaximumHeight(320)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(self.table_style())

        tbl_layout.addWidget(self.table)
        table_card.setLayout(tbl_layout)

        main_layout.addWidget(table_card)
        main_layout.addStretch()

        container.setLayout(main_layout)
        scroll.setWidget(container)
        outer_layout.addWidget(scroll)
        self.setLayout(outer_layout)

        self.load_data()

    # ================= CHART FRAME =================
    def create_chart_frame(self, title_text):
        frame = QFrame()
        frame.setObjectName("chartFrame")
        frame.setStyleSheet("""
            QFrame#chartFrame {
                background-color: #1E293B;
                border-radius: 12px;
            }
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(14, 12, 14, 10)
        layout.setSpacing(4)

        title = QLabel(title_text)
        title.setStyleSheet(
            "font-size: 14px; font-weight: bold; color: #CBD5E1; "
            "background: transparent; border: none; padding: 0;"
        )
        layout.addWidget(title)
        frame.setLayout(layout)
        return frame

    # ================= LOAD DATA =================
    def load_data(self):
        products = self.inventory_controller.get_all_products()
        sales = self.sales_controller.get_sales()

        total_products = len(products)
        total_revenue = sum(s.get("total_price", 0) for s in sales)
        total_transactions = len(sales)

        today = datetime.now().strftime("%Y-%m-%d")
        today_revenue = sum(
            s.get("total_price", 0) for s in sales
            if today in s.get("sale_date", "")
        )

        # Animate card counters
        self.products_card.animate_to(int(total_products))
        self.revenue_card.animate_to(int(total_revenue), is_currency=True)
        self.transactions_card.animate_to(int(total_transactions))
        self.today_card.animate_to(int(today_revenue), is_currency=True)

        self.plot_bar_chart(sales)
        self.plot_donut_chart(sales, products)
        self.plot_area_chart(sales)
        self.load_table(sales)

    # ================================================================
    #  BAR CHART with hover highlight
    # ================================================================
    def plot_bar_chart(self, sales):
        product_revenue = defaultdict(float)
        product_qty = defaultdict(int)
        for s in sales:
            name = s.get("product_name", "Unknown")
            product_revenue[name] += s.get("total_price", 0)
            product_qty[name] += s.get("quantity", 0)

        sorted_items = sorted(product_revenue.items(), key=lambda x: x[1], reverse=True)[:8]
        if not sorted_items:
            return

        names = [item[0] for item in sorted_items]
        revenues = [item[1] for item in sorted_items]
        qtys = [product_qty[n] for n in names]

        fig = self.bar_canvas.figure
        fig.clear()
        fig.set_facecolor("#1E293B")

        ax = fig.add_subplot(111)
        ax.set_facecolor("#1E293B")

        colors = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444",
                  "#8B5CF6", "#EC4899", "#06B6D4", "#F97316"]
        bar_colors = [colors[i % len(colors)] for i in range(len(names))]

        bars = ax.barh(names, revenues, color=bar_colors, height=0.55,
                       edgecolor="none", zorder=3)

        self._bar_original_colors = list(bar_colors)

        ax.set_axisbelow(True)
        ax.xaxis.grid(True, color="#293548", linewidth=0.5, linestyle="--", alpha=0.5)

        max_rev = max(revenues) if revenues else 1
        self._bar_value_texts = []
        for bar, val in zip(bars, revenues):
            txt = ax.text(
                bar.get_width() + max_rev * 0.03,
                bar.get_y() + bar.get_height() / 2,
                f"₹{val:,.0f}",
                va="center", ha="left",
                color="#94A3B8", fontsize=9, fontweight="bold"
            )
            self._bar_value_texts.append(txt)

        ax.invert_yaxis()
        ax.tick_params(axis="y", colors="#CBD5E1", labelsize=10, length=0, pad=8)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.xaxis.set_visible(False)
        ax.set_xlim(0, max_rev * 1.3)

        fig.tight_layout(pad=0.8)
        self.bar_canvas.draw()

        # Store data for hover
        self._bar_data = {
            "ax": ax, "bars": bars, "names": names,
            "revenues": revenues, "qtys": qtys, "fig": fig
        }
        self._bar_hover_idx = -1

        # Connect hover event
        try:
            self.bar_canvas.mpl_disconnect(self._bar_cid)
        except (AttributeError, TypeError):
            pass
        self._bar_cid = self.bar_canvas.mpl_connect("motion_notify_event", self._on_bar_hover)
        self._bar_leave_cid = self.bar_canvas.mpl_connect("axes_leave_event", self._on_bar_leave)

    def _on_bar_hover(self, event):
        if event.inaxes != self._bar_data.get("ax"):
            self._reset_bar_colors()
            self.bar_tooltip.hide()
            return

        bars = self._bar_data["bars"]
        hit_idx = -1

        for i, bar in enumerate(bars):
            if bar.contains(event)[0]:
                hit_idx = i
                break

        if hit_idx == self._bar_hover_idx:
            return

        self._bar_hover_idx = hit_idx
        self._reset_bar_colors()

        if hit_idx >= 0:
            # Dim all bars except hovered
            for i, bar in enumerate(bars):
                if i == hit_idx:
                    bar.set_alpha(1.0)
                    bar.set_edgecolor("white")
                    bar.set_linewidth(1.5)
                else:
                    bar.set_alpha(0.3)

            name = self._bar_data["names"][hit_idx]
            rev = self._bar_data["revenues"][hit_idx]
            qty = self._bar_data["qtys"][hit_idx]
            tooltip_text = f"{name}\n₹{rev:,.2f}  •  {qty} units sold"

            # Position tooltip
            canvas_pos = self.bar_canvas.mapToGlobal(
                QPoint(int(event.x), int(self.bar_canvas.height() - event.y))
            )
            self.bar_tooltip.show_at(tooltip_text, canvas_pos, self.bar_canvas)

            self.bar_canvas.draw_idle()
        else:
            self.bar_tooltip.hide()

    def _on_bar_leave(self, event):
        self._reset_bar_colors()
        self.bar_tooltip.hide()
        self._bar_hover_idx = -1

    def _reset_bar_colors(self):
        if "bars" not in self._bar_data:
            return
        for i, bar in enumerate(self._bar_data["bars"]):
            bar.set_alpha(1.0)
            bar.set_edgecolor("none")
            bar.set_linewidth(0)
        self.bar_canvas.draw_idle()

    # ================================================================
    #  DONUT CHART with hover explode
    # ================================================================
    def plot_donut_chart(self, sales, products):
        product_category = {}
        for p in products:
            product_category[p.get("product_name", "")] = p.get("category", "Other")

        category_revenue = defaultdict(float)
        for s in sales:
            name = s.get("product_name", "Unknown")
            cat = product_category.get(name, "Other")
            category_revenue[cat] += s.get("total_price", 0)

        if not category_revenue:
            return

        sorted_cats = sorted(category_revenue.items(), key=lambda x: x[1], reverse=True)
        labels = [c[0] for c in sorted_cats]
        values = [c[1] for c in sorted_cats]

        fig = self.donut_canvas.figure
        fig.clear()
        fig.set_facecolor("#1E293B")

        ax = fig.add_subplot(111)
        ax.set_facecolor("#1E293B")

        colors = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444",
                  "#8B5CF6", "#EC4899", "#06B6D4", "#F97316"]
        slice_colors = [colors[i % len(colors)] for i in range(len(labels))]

        wedges, texts, autotexts = ax.pie(
            values, labels=None,
            autopct=lambda pct: f"{pct:.0f}%" if pct > 5 else "",
            startangle=90, colors=slice_colors,
            wedgeprops=dict(width=0.42, edgecolor="#1E293B", linewidth=2.5),
            pctdistance=0.78,
            textprops={"fontsize": 9, "fontweight": "bold"}
        )

        for t in autotexts:
            t.set_color("white")
            t.set_path_effects([
                patheffects.withStroke(linewidth=2, foreground="#1E293B")
            ])

        total = sum(values)
        self._donut_center_text = ax.text(
            0, 0.06, f"₹{total:,.0f}", ha="center", va="center",
            fontsize=14, fontweight="bold", color="#F1F5F9"
        )
        ax.text(0, -0.12, "Total", ha="center", va="center",
                fontsize=9, color="#64748B")

        legend = ax.legend(
            wedges, labels, loc="upper center",
            bbox_to_anchor=(0.5, -0.02),
            ncol=min(3, len(labels)),
            frameon=False, fontsize=9, labelcolor="#94A3B8"
        )

        fig.tight_layout(pad=0.5)
        self.donut_canvas.draw()

        # Store for hover
        self._donut_data = {
            "ax": ax, "wedges": wedges, "labels": labels,
            "values": values, "total": total, "fig": fig,
            "autotexts": autotexts, "slice_colors": slice_colors
        }
        self._donut_hover_idx = -1

        try:
            self.donut_canvas.mpl_disconnect(self._donut_cid)
        except (AttributeError, TypeError):
            pass
        self._donut_cid = self.donut_canvas.mpl_connect("motion_notify_event", self._on_donut_hover)
        self._donut_leave_cid = self.donut_canvas.mpl_connect("axes_leave_event", self._on_donut_leave)

    def _on_donut_hover(self, event):
        if event.inaxes != self._donut_data.get("ax"):
            self._reset_donut()
            self.donut_tooltip.hide()
            return

        wedges = self._donut_data["wedges"]
        hit_idx = -1

        for i, w in enumerate(wedges):
            hit, _ = w.contains(event)
            if hit:
                hit_idx = i
                break

        if hit_idx == self._donut_hover_idx:
            return

        self._donut_hover_idx = hit_idx
        self._reset_donut()

        if hit_idx >= 0:
            # Dim other slices
            for i, w in enumerate(wedges):
                if i == hit_idx:
                    w.set_alpha(1.0)
                    w.set_linewidth(3)
                    w.set_edgecolor("white")
                else:
                    w.set_alpha(0.35)

            label = self._donut_data["labels"][hit_idx]
            val = self._donut_data["values"][hit_idx]
            total = self._donut_data["total"]
            pct = (val / total * 100) if total > 0 else 0

            # Update center text
            self._donut_center_text.set_text(f"₹{val:,.0f}")

            tooltip_text = f"{label}\n₹{val:,.2f} ({pct:.1f}%)"
            canvas_pos = self.donut_canvas.mapToGlobal(
                QPoint(int(event.x), int(self.donut_canvas.height() - event.y))
            )
            self.donut_tooltip.show_at(tooltip_text, canvas_pos, self.donut_canvas)

            self.donut_canvas.draw_idle()
        else:
            self.donut_tooltip.hide()

    def _on_donut_leave(self, event):
        self._reset_donut()
        self.donut_tooltip.hide()
        self._donut_hover_idx = -1

    def _reset_donut(self):
        if "wedges" not in self._donut_data:
            return
        for i, w in enumerate(self._donut_data["wedges"]):
            w.set_alpha(1.0)
            w.set_linewidth(2.5)
            w.set_edgecolor("#1E293B")
        # Reset center text
        total = self._donut_data.get("total", 0)
        if hasattr(self, "_donut_center_text"):
            self._donut_center_text.set_text(f"₹{total:,.0f}")
        self.donut_canvas.draw_idle()

    # ================================================================
    #  AREA CHART with hover crosshair
    # ================================================================
    def plot_area_chart(self, sales):
        today = datetime.now().date()
        dates = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
        date_strs = [d.strftime("%Y-%m-%d") for d in dates]
        display_labels = [d.strftime("%b %d") for d in dates]

        daily_revenue = defaultdict(float)
        daily_txns = defaultdict(int)
        for s in sales:
            sale_date = s.get("sale_date", "")[:10]
            if sale_date in date_strs:
                daily_revenue[sale_date] += s.get("total_price", 0)
                daily_txns[sale_date] += 1

        revenue_values = [daily_revenue.get(d, 0) for d in date_strs]
        txn_counts = [daily_txns.get(d, 0) for d in date_strs]

        fig = self.area_canvas.figure
        fig.clear()
        fig.set_facecolor("#1E293B")

        ax = fig.add_subplot(111)
        ax.set_facecolor("#1E293B")

        x = np.arange(len(display_labels))

        # Gradient-like area fill using multiple alphas
        ax.fill_between(x, revenue_values, alpha=0.12, color="#3B82F6", zorder=2)
        ax.fill_between(x, [v * 0.5 for v in revenue_values], alpha=0.08, color="#3B82F6", zorder=2)

        line, = ax.plot(
            x, revenue_values, color="#3B82F6", linewidth=2.5,
            marker="o", markersize=7, markerfacecolor="#3B82F6",
            markeredgecolor="#1E293B", markeredgewidth=2, zorder=4
        )

        # Static value labels for non-zero points
        for i, val in enumerate(revenue_values):
            if val > 0:
                ax.annotate(
                    f"₹{val:,.0f}", (x[i], val),
                    textcoords="offset points", xytext=(0, 14),
                    ha="center", va="bottom", fontsize=8, fontweight="bold",
                    color="#60A5FA",
                    bbox=dict(boxstyle="round,pad=0.25", facecolor="#1E293B",
                              edgecolor="#2A3A55", linewidth=0.8)
                )

        # Crosshair line (initially invisible)
        self._crosshair_line = ax.axvline(x=0, color="#3B82F6", linewidth=1,
                                           linestyle="--", alpha=0, zorder=5)
        self._crosshair_dot, = ax.plot([], [], "o", color="#60A5FA",
                                        markersize=10, markeredgecolor="white",
                                        markeredgewidth=2, zorder=6, alpha=0)

        ax.set_axisbelow(True)
        ax.yaxis.grid(True, color="#293548", linewidth=0.5, linestyle="--", alpha=0.5)
        ax.set_xticks(x)
        ax.set_xticklabels(display_labels)
        ax.tick_params(axis="x", colors="#94A3B8", labelsize=10, length=0, pad=8)
        ax.tick_params(axis="y", colors="#475569", labelsize=9, length=0, pad=6)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(
            lambda val, pos: f"₹{val:,.0f}" if val > 0 else "0"
        ))
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_color("#334155")
        ax.spines["left"].set_visible(False)
        ax.set_ylim(bottom=0)

        fig.tight_layout(pad=1.2)
        self.area_canvas.draw()

        # Store for hover
        self._line_data = {
            "ax": ax, "x": x, "revenues": revenue_values,
            "txns": txn_counts, "labels": display_labels, "fig": fig,
            "line": line
        }
        self._line_hover_idx = -1

        try:
            self.area_canvas.mpl_disconnect(self._line_cid)
        except (AttributeError, TypeError):
            pass
        self._line_cid = self.area_canvas.mpl_connect("motion_notify_event", self._on_line_hover)
        self._line_leave_cid = self.area_canvas.mpl_connect("axes_leave_event", self._on_line_leave)

    def _on_line_hover(self, event):
        if event.inaxes != self._line_data.get("ax"):
            self._reset_line()
            self.line_tooltip.hide()
            return

        x_arr = self._line_data["x"]
        # Find nearest x index
        if event.xdata is None:
            return

        nearest_idx = int(np.clip(round(event.xdata), 0, len(x_arr) - 1))

        if nearest_idx == self._line_hover_idx:
            return

        self._line_hover_idx = nearest_idx

        rev = self._line_data["revenues"][nearest_idx]
        txn = self._line_data["txns"][nearest_idx]
        label = self._line_data["labels"][nearest_idx]

        # Show crosshair
        self._crosshair_line.set_xdata([x_arr[nearest_idx]])
        self._crosshair_line.set_alpha(0.6)

        self._crosshair_dot.set_data([x_arr[nearest_idx]], [rev])
        self._crosshair_dot.set_alpha(1.0)

        tooltip_text = f"{label}\n₹{rev:,.2f}  •  {txn} sales"
        canvas_pos = self.area_canvas.mapToGlobal(
            QPoint(int(event.x), int(self.area_canvas.height() - event.y))
        )
        self.line_tooltip.show_at(tooltip_text, canvas_pos, self.area_canvas)

        self.area_canvas.draw_idle()

    def _on_line_leave(self, event):
        self._reset_line()
        self.line_tooltip.hide()
        self._line_hover_idx = -1

    def _reset_line(self):
        if hasattr(self, "_crosshair_line"):
            self._crosshair_line.set_alpha(0)
        if hasattr(self, "_crosshair_dot"):
            self._crosshair_dot.set_alpha(0)
        self.area_canvas.draw_idle()

    # ================= TABLE =================
    def load_table(self, sales):
        recent_sales = sales[-10:]
        self.table.setRowCount(len(recent_sales))

        for row, s in enumerate(recent_sales):
            product_item = QTableWidgetItem(s.get("product_name", ""))
            qty_item = QTableWidgetItem(str(s.get("quantity", "")))
            total_item = QTableWidgetItem(f"₹{s.get('total_price', 0):,.2f}")
            date_item = QTableWidgetItem(s.get("sale_date", ""))

            qty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            total_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.table.setItem(row, 0, product_item)
            self.table.setItem(row, 1, qty_item)
            self.table.setItem(row, 2, total_item)
            self.table.setItem(row, 3, date_item)

        for row in range(self.table.rowCount()):
            self.table.setRowHeight(row, 36)

    # ================= STYLES =================
    def scroll_style(self):
        return """
            QScrollArea#pageScroll {
                background-color: #0F172A;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #0F172A;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #334155;
                border-radius: 4px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #475569;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical,
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
                border: none;
            }
        """

    def table_style(self):
        return """
            QTableWidget {
                background-color: #1E293B;
                color: #E2E8F0;
                border: none;
                font-size: 13px;
                gridline-color: transparent;
            }
            QHeaderView::section {
                background-color: #273449;
                color: #F1F5F9;
                padding: 8px 12px;
                border: none;
                font-weight: bold;
                font-size: 13px;
                min-height: 20px;
            }
            QTableWidget::item {
                padding: 6px 10px;
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
                background-color: #334155;
                border-radius: 4px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #475569;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical,
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
                border: none;
            }
        """
