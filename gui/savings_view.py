import tkinter as tk
from tkinter import ttk
from colors import *

def view_savings(root, content_box, logic):
    # container
    split_container = tk.Frame(content_box, bg=COLOR_CONTENT_BG)
    split_container.pack(fill="both", expand=True, padx=10, pady=10)
    
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
        "font": ("Calibri", 14)
    }

    # page title
    page_title = tk.Label(
        left_frame, 
        text="Add Target Savings",
        font=("Calibri", 18, "bold"),
        bg=COLOR_CONTENT_BG
    )
    page_title.pack(pady=(20, 20),anchor="w", padx=20)

    # item
    item_label = tk.Label(
        left_frame,
        text="Item Name:",
        bg=COLOR_CONTENT_BG,
        font=("Calibri", 14, "bold")
    )
    item_label.pack(anchor="w", padx=20)

    item_input = tk.Entry(left_frame, **input_style)
    item_input.pack(fill="x", padx=20, pady=(0, 15), ipady=4)

    # cost
    cost_label = tk.Label(
        left_frame,
        text="Cost (₱):",
        bg=COLOR_CONTENT_BG,
        font=("Calibri", 14, "bold")
    )
    cost_label.pack(anchor="w", padx=20)

    cost_input = tk.Entry(left_frame, **input_style)
    cost_input.pack(fill="x", padx=20, pady=(0, 15), ipady=4)

    # target date
    target_label = tk.Label(
        left_frame,
        text="Target Date (MM/DD/YYYY):",
        bg=COLOR_CONTENT_BG,
        font=("Calibri", 14, "bold")
    )
    target_label.pack(anchor="w", padx=20)

    target_input = tk.Entry(left_frame, **input_style)
    target_input.pack(fill="x", padx=20, pady=(0, 25), ipady=4)

    def handle_submit():
        try:
            item = item_input.get()
            cost = cost_input.get()
            date = target_input.get()

            if not item and cost and date:
                tk.messagebox.showwarning("Error", "Invalid Input.")
            else:
                logic.add_target(item, float(cost), date) # Send to OOP controller
                refresh_cards()                   # Redraw the screen
                
                # Clear input boxes
                item_input.delete(0, tk.END)
                cost_input.delete(0, tk.END)
                target_input.delete(0, tk.END)
        except ValueError:
            tk.messagebox.showwarning("Error", "Invalid Input.")


    target_button = tk.Button(
        left_frame,
        text="Add Target",
        bg=COLOR_SIDEBAR,
        font=("Calibri", 14, "bold"),
        fg="white",
        bd=0,
        padx=15,
        pady=8,
        command=handle_submit
    )
    target_button.pack(fill="x", padx=20)

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
    canvas = tk.Canvas(right_frame, bg=COLOR_CONTENT_BG, highlightthickness=0)

    # scroll bar
    scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)

    # Frame for the cards in the canvas
    target_grid = tk.Frame(canvas, bg=COLOR_CONTENT_BG)

    # determines how long the list for the scrolling
    target_grid.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # put frame inside canvas window
    canvas_window = canvas.create_window((0, 0), window=target_grid, anchor="nw")

    # link scrollbar and canvas
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    canvas.bind(
        "<Configure>",
        lambda e: canvas.itemconfig(canvas_window, width=e.width)
    )

    def handle_card_action(action, target_id):
        if action == "remove":
            response  = tk.messagebox.askyesno("Delete", "Are you sure you want to delete?")
            if response:
                logic.remove_target(target_id)  # Call the logic to remove income
                refresh_cards()  # Refresh the cards to reflect changes
        elif action == "edit":
            # Logic for editing income can be added here
            print(f"Edit action triggered for target ID: {target_id}")


    def create_target_card(parent, row, col, target_id, name, cost_str, saved_str, needed_str, progress_val, date):

        # card
        card = tk.Frame(parent, bg=COLOR_CARD_BG, highlightbackground=COLOR_BORDER)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1) 
        
        # tiny frame on the top of the card
        top_row = tk.Frame(card, bg=COLOR_CARD_BG)
        top_row.pack(fill="x", padx=10, pady=(10, 5))
        
        # name
        name_label = tk.Label(
            top_row,
            text=name.upper(),
            font=("Calibri", 10, "bold"),
            fg="black",
            bg=COLOR_CARD_BG
        )
        name_label.pack(side="left")

        # remove button
        remove_button = tk.Button(
            top_row,
            text="Remove",
            font=("Calibri", 10),
            fg="red",
            bg=COLOR_CARD_BG,
            bd=0, cursor="hand2",
            command=lambda: handle_card_action("remove", target_id)
        )
        remove_button.pack(side="right")

        # edit button
        edit_button = tk.Button(
            top_row, 
            text="Edit",
            font=("Calibri", 10),
            fg="#64748B",
            bg=COLOR_CARD_BG,
            bd=0, cursor="hand2",
            command=lambda: handle_card_action("edit", target_id)
        )
        edit_button.pack(side="right", padx=5)

        # saved button
        saved_button = tk.Button(
            top_row,
            text="Add Funds",
            font=("Calibri", 10),
            fg="green",
            bg=COLOR_CARD_BG,
            bd=0, cursor="hand2"
        )
        saved_button.pack(side="right")

        # cost
        cost_label = tk.Label(
            card,
            text=f"₱{cost_str:,.2f}",
            font=("Calibri", 20, "bold"),
            fg="black", bg=COLOR_CARD_BG
        )
        cost_label.pack(anchor="w", padx=10)

        # description
        saved_label = tk.Label(
            card,
            text=f"Saved: ₱{saved_str:,.2f}",
            font=("Calibri", 12),
            fg="#555555",
            bg=COLOR_CARD_BG
        )
        saved_label.pack(anchor="w", padx=10)
        
        # description
        needed_label = tk.Label(
            card,
            text=f"Needed: ₱{needed_str:,.2f}",
            font=("Calibri", 12),
            fg="#555555",
            bg=COLOR_CARD_BG
        )
        needed_label.pack(anchor="w", padx=10)

        # progress bar
        progress = ttk.Progressbar(
            card,
            style="TProgressbar",
            orient="horizontal",
            length=200,
            mode="determinate"
        )
        progress.pack(fill="x", padx=10, pady=(0, 5))
        progress["value"] = progress_val # Purely visual value passed in

        # goal date
        goal_label = tk.Label(
            card,
            text=f"Goal Date: {date}",
            font=("Calibri", 10),
            fg="#888888",
            bg=COLOR_CARD_BG
        )
        goal_label.pack(anchor="w", padx=10, pady=(5, 15))

    def refresh_cards():
        # Clear all existing savings cards 
        for existing_card_widget in target_grid.winfo_children():
            existing_card_widget.destroy()

        # get all the savings data 
        current_savings_list = logic.get_savings()

        # Create and display a new card for each income
        for savings_index in range(len(current_savings_list)):
            # get the actual savings item from list using its current index.
            target_savings = current_savings_list[savings_index]

            # 1 card per row
            target_row = savings_index 
            target_column = 0

            # call a separate function to visually create one income card.
            create_target_card(
                parent=target_grid,
                row=target_row,
                col=target_column,
                target_id=target_savings.get_target_id(),
                name=target_savings.get_name(),
                cost_str=target_savings.get_cost(),
                saved_str=target_savings.get_saved(),
                needed_str=target_savings.get_needed(),
                progress_val=target_savings.get_progress(),
                date=target_savings.get_date()
            )
    refresh_cards()

