import tkinter as tk
from colors import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from logic.controller import TrakkiLogic

logic = TrakkiLogic()

# Global reference to store the content box for refreshing
_dashboard_content_box = None

def view_dashboard(root, content_box, logic):
    global _dashboard_content_box
    _dashboard_content_box = content_box
    
    # Initial render
    refresh_dashboard(logic)

def refresh_dashboard(logic):
    global _dashboard_content_box
    if _dashboard_content_box is None:
        return

    # Clear the content box before rebuilding
    for widget in _dashboard_content_box.winfo_children():
        widget.destroy()

    # Header frame (the one with filtering)
    header_frame = tk.Frame(
        _dashboard_content_box,
        bg=COLOR_CONTENT_BG
    )
    header_frame.pack(fill="x", padx=20, pady=10)

    title = tk.Label(
        header_frame, 
        text="Financial Overview",
        font=("Calibri", 16, "bold"),
        bg=COLOR_CONTENT_BG
    )
    title.pack(side="left")

    filter_frame = tk.Frame(
        header_frame,
        bg=COLOR_CARD_BG,
        highlightbackground=COLOR_BORDER
    )
    filter_frame.pack(side="right")

    # timeframes list
    timeframes = ["Daily", "Weekly", "Monthly", "Yearly"]

    for tf in timeframes:

        timeframe_btn = tk.Button(
            filter_frame,
            text=tf,
            font=("Calibri", 9, "bold"),
            bg="white",
            fg="#555555",
            bd=0,
            padx=15,
            pady=6,
            cursor="hand2"
        )
        timeframe_btn.pack(side="left")

    # containers (cards)
    cards_frame = tk.Frame(
        _dashboard_content_box,
        bg=COLOR_CONTENT_BG
    )
    cards_frame.pack(fill="x", padx=20, pady=(0, 20))
    cards_frame.grid_rowconfigure(0, weight=1)

    chart_frame = tk.Frame(
        _dashboard_content_box,
        bg=COLOR_CONTENT_BG,
        highlightbackground=COLOR_BORDER
    )
    chart_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))

    # function for creating cards container
    def create_container_card(parent, col, title, text_val, value_color="black"):
        # frame
        card = tk.Frame(
            parent,
            bg=COLOR_CARD_BG,
            highlightbackground=COLOR_BORDER
        )
        card.grid(row=0, column=col, padx=10, pady=10, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)
        
        # label
        container_label = tk.Label(
            card,
            text=title,
            font=("Calibri", 11),
            bg=COLOR_CARD_BG,
            fg="#555555"
        )
        container_label.pack(expand=True, side="bottom", pady=(0, 10))

        value_label = tk.Label(
            card, 
            text=text_val,
            font=("Calibri", 18, "bold"),
            bg=COLOR_CARD_BG,
            fg=value_color
        )
        value_label.pack(expand=True, side="top", pady=(10, 0))

    # static UI Cards
    create_container_card(cards_frame, 0, "Current Balance", f"₱{logic.current_balance():,.2f}", COLOR_SIDEBAR_ACTIVE)
    create_container_card(cards_frame, 1, "Total Income", f"₱{logic.total_income():,.2f}", "green")
    create_container_card(cards_frame, 2, "Total Expenses", f"₱{logic.total_expenses():,.2f}", "#EF4444")
    create_container_card(cards_frame, 3, "Total Saved", f"₱{logic.total_saved():,.2f}", "black")

    # matplotlib static Charts
    chart_area, bars_pos = plt.subplots(figsize=(8, 4), dpi=100)
    chart_area.patch.set_facecolor(COLOR_CONTENT_BG)
    bars_pos.set_facecolor(COLOR_CONTENT_BG)

    # categories list
    categories = ['Income', 'Expenses', 'Target Savings']
    
    # amounts list (with logic data)
    amounts = [logic.total_income(), logic.total_expenses(), logic.total_saved()]

    # bar colors
    bar_colors = [COLOR_SIDEBAR_ACTIVE, "#EF4444", "#10B981"]

    # draws a bar for each category
    bars = bars_pos.bar(categories, amounts, color=bar_colors, width=0.5)

    bars_pos.spines['top'].set_visible(False) # remove top border
    bars_pos.spines['right'].set_visible(False) # remove right border
    bars_pos.spines['left'].set_color(COLOR_BORDER)
    bars_pos.spines['bottom'].set_color(COLOR_BORDER)
    bars_pos.tick_params(colors="#64748B")
    bars_pos.set_title('Cash Flow Overview', color=COLOR_SIDEBAR, pad=20, fontsize=14, fontweight='bold')

    for bar in bars:
        y_value = bar.get_height()
        if y_value > 0:  # Only show label if there's a value
            bars_pos.text(bar.get_x() + bar.get_width()/2, y_value + 100, f'₱{y_value:,.0f}', ha='center', va='bottom', color=COLOR_SIDEBAR, fontweight='bold')

    canvas = FigureCanvasTkAgg(chart_area, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)