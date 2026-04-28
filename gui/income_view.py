import tkinter as tk
from tkinter import ttk
from colors import *

def view_income(root, content_box, logic):
    # container
    split_container = tk.Frame(content_box, bg=COLOR_CONTENT_BG)
    split_container.pack(fill="both", expand=True, padx=10, pady=10)

    # divide the container into two (column 0 and 1)
    split_container.grid_columnconfigure(0, weight=1, uniform="equal")
    split_container.grid_columnconfigure(1, weight=1, uniform="equal")
    split_container.grid_rowconfigure(0, weight=1)

    # left frame
    left_frame = tk.Frame(
        split_container,
        bg=COLOR_CONTENT_BG,
        highlightbackground=COLOR_BORDER
    )
    left_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)

    # a dictionary to store the design of the input boxes
    input_style = {
        "highlightthickness": 1,
        "highlightbackground": "#CBD5E1",
        "highlightcolor": COLOR_SIDEBAR_ACTIVE,
        "relief": "flat", # visual style of the border
        "bd": 1,
        "font": ("Calibri", 16)
    }

    # page title
    page_title = tk.Label(
        left_frame,
        text="Add New Income",
        font=("Calibri", 20, "bold"),
        bg = COLOR_CONTENT_BG
    )
    page_title.pack(pady=20, anchor="w", padx=20)

    # Amount input Field
    amount_label = tk.Label(
        left_frame,
        text="Amount:",
        bg=COLOR_CONTENT_BG,
        font=("Calibri", 18, "bold")
    )
    amount_label.pack(anchor="w", padx=20)

    amount_input = tk.Entry(left_frame, **input_style)
    amount_input.pack(fill="x", padx=20, pady=(0, 15), ipady=2)

    # category input field
    category_label = tk.Label(
        left_frame,
        text="Category:",
        bg=COLOR_CONTENT_BG,
        font=("Calibri", 18, "bold")
    )
    category_label.pack(anchor="w", padx=20)

    category_input = tk.Entry(left_frame, **input_style)
    category_input.pack(fill="x", padx=20, pady=(0, 15), ipady=2)

    # descrioption input field
    description_label = tk.Label(
        left_frame,
        text="Description:",
        bg=COLOR_CONTENT_BG,
        font=("Calibri", 18, "bold")
    )
    description_label.pack(anchor="w", padx=20)

    description_input = tk.Text(left_frame, height=6, wrap="word", **input_style)
    description_input.pack(fill="x", padx=20, pady=(0, 25))

    def handle_submit():
        amount = amount_input.get()
        category = category_input.get()
        desc = description_input.get("1.0", "end-1c")

        if amount and category:
            logic.add_income(amount, category, desc) # Send to OOP controller
            refresh_cards() # Redraw the screen
            
            # Clear input boxes
            amount_input.delete(0, tk.END)
            category_input.delete(0, tk.END)
            description_input.delete('1.0', tk.END)

    submit_button = tk.Button(
        left_frame,
        text="Add Income",
        bg=COLOR_SIDEBAR,
        font=("Calibri", 18, "bold"),
        fg="white",
        bd=0,
        padx=15,
        pady=8,
        command=handle_submit
    )
    submit_button.pack(fill="x", padx=20)

    # right frame
    right_frame = tk.Frame(
        split_container,
        bg=COLOR_CONTENT_BG
    )
    right_frame.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=(5, 10),
        pady=10
    )

    # Canvas - frame that can move up and down
    canvas = tk.Canvas(
        right_frame,
        bg=COLOR_CONTENT_BG,
        highlightthickness=0
    )

    # scrollbar for the canvas
    scrollbar = ttk.Scrollbar(
        right_frame,
        orient='vertical',
        command=canvas.yview
    )

    # Frame for the cards in the canvas
    income_grid = tk.Frame(
        canvas,
        bg=COLOR_CONTENT_BG
    )

    # determines how long the list for the scrolling
    income_grid.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # put frame inside canvas window
    canvas_window = canvas.create_window(
        (0,0),
        window=income_grid,
        anchor="nw"
    )

    # link scrollbar and canvas
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    canvas.bind(
        "<Configure>",
        lambda e: canvas.itemconfig(canvas_window, width=e.width)
    )

    def create_income_card(parent, row, col, amount, category, desc, date):

        # card
        card = tk.Frame(parent, bg=COLOR_CARD_BG, highlightbackground=COLOR_BORDER)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)

        # tiny frame on the top of the card
        top_row = tk.Frame(card, bg=COLOR_CARD_BG)
        top_row.pack(fill="x", padx=10, pady=(10, 5))

        # category
        c_label = tk.Label(
            top_row,
            text=category.upper(),
            font=("Calibri", 9, "bold"),
            fg="#10B981",
            bg=COLOR_CARD_BG,
        )
        c_label.pack(side="left")

        # Remove Button
        t_button = tk.Button(
            top_row,
            text="Remove",
            font=("Calibri", 10),
            fg="#EF4444",
            bg=COLOR_CARD_BG,
            bd=0,
            cursor="hand2"
        )
        t_button.pack(side="right")

        # Edit button 
        e_button = tk.Button(
            top_row,
            text="Edit",
            font=("Calibri", 10),
            fg="#64748B",
            bg=COLOR_CARD_BG,
            bd=0,
            cursor="hand2"
        )
        e_button.pack(side="right", padx=5)

        # Card Details
        amount_details = tk.Label(
            card,
            text=f"₱{float(str(amount)):,.2f}",
            font=("Calibri", 20, "bold"),
            fg="black",
            bg=COLOR_CARD_BG
        )
        amount_details.pack(anchor="w", padx=10)

        desc_details = tk.Label(
            card,
            text=desc,
            font=("Calibri", 12),
            fg="#333333",
            bg=COLOR_CARD_BG,
            justify="left",
            wraplength=200
        )
        desc_details.pack(anchor="w", padx=10, pady=(5, 0))

        date_details = tk.Label(
            card,
            text=date,
            font=("Calibri", 10),
            fg="#888888",
            bg=COLOR_CARD_BG
        )
        date_details.pack(anchor="w", padx=10, pady=(10, 15))

    def refresh_cards():
        # Clear all existing income cards 
        for existing_card_widget in income_grid.winfo_children():
            existing_card_widget.destroy()

        # get all the incomes data 
        current_incomes_list = logic.get_incomes()

        # Create and display a new card for each income
        for income_index in range(len(current_incomes_list)):
            # get the actual income item from list using its current index.
            income_item = current_incomes_list[income_index]

            # calculate which row this card should go into.
            target_row = income_index // 2  # Integer division by 2

            # Calculate which column this card should go into.
            target_column = income_index % 2 # Modulo 2 gives remainder (0 or 1)

            # call a separate function to visually create one income card.
            create_income_card(
                parent=income_grid,
                row=target_row,
                col=target_column,
                amount=income_item.get_amount(),
                category=income_item.get_category(),
                desc=income_item.get_desc(),
                date=income_item.get_date()
            )
    refresh_cards()