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
    left_frame = tk.Frame(split_container, bg=COLOR_CONTENT_BG, highlightbackground=COLOR_BORDER)
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
    page_title = tk.Label(left_frame, text="Add Target Savings", font=("Calibri", 18, "bold"), bg=COLOR_CONTENT_BG)
    page_title.pack(pady=(20, 20), anchor="w", padx=20)

    # item
    item_label = tk.Label(left_frame, text="Item Name:", bg=COLOR_CONTENT_BG, font=("Calibri", 14, "bold"))
    item_label.pack(anchor="w", padx=20)
    item_input = tk.Entry(left_frame, **input_style)
    item_input.pack(fill="x", padx=20, pady=(0, 15), ipady=4)

    # cost
    cost_label = tk.Label(left_frame, text="Cost (₱):", bg=COLOR_CONTENT_BG, font=("Calibri", 14, "bold"))
    cost_label.pack(anchor="w", padx=20)
    cost_input = tk.Entry(left_frame, **input_style)
    cost_input.pack(fill="x", padx=20, pady=(0, 15), ipady=4)

    # target date
    target_label = tk.Label(left_frame, text="Target Date (MM/DD/YYYY):", bg=COLOR_CONTENT_BG, font=("Calibri", 14, "bold"))
    target_label.pack(anchor="w", padx=20)
    target_input = tk.Entry(left_frame, **input_style)
    target_input.pack(fill="x", padx=20, pady=(0, 10), ipady=4)

    # function for clearing input fields
    def clear_fields():
        item_input.delete(0, tk.END)
        cost_input.delete(0, tk.END)
        target_input.delete(0 , tk.END)

    def reset_form():
        clear_fields()
        editing_id[0] = None
        page_title.config(text="Add New Target")
        submit_button.config(text="Add Target")
        cancel_button.pack_forget()  # Hide the cancel button

    editing_id = [None]

    def handle_submit():
        item = item_input.get()
        cost = cost_input.get()
        date = target_input.get()

        # Checks if all fields are not empty
        if not item or not cost or not date:
            tk.messagebox.showwarning("Error", "All Fields are required.")
            return
        # catches unvalid number
        try:
            if editing_id[0]:
                logic.update_target(editing_id[0], item, cost, date)
                tk.messagebox.showinfo("Success", "Update Target Successful!")
            else:
                logic.add_target(item, cost, date)
                tk.messagebox.showinfo("Success", "Add Target Successful!")
        except ValueError:
            tk.messagebox.showwarning("Error", "Cost must be a number.")
            return

        refresh_cards()
        reset_form()

    # Pack the submit button
    submit_button = tk.Button(left_frame, text="Add Target", bg=COLOR_SIDEBAR, font=("Calibri", 14, "bold"), fg="white", bd=0, padx=15, pady=8, command=handle_submit)
    submit_button.pack(fill="x", padx=20, pady=(10, 5)) 

    # Pack the cancel button
    cancel_button = tk.Button(left_frame, text="Cancel", bg="#EF4444", font=("Calibri", 14, "bold"), fg="white", bd=0, padx=15, pady=8, command=reset_form)
    cancel_button.pack(fill="x", padx=20, pady=(0, 10)) 
    
    # Total Balance Card
    balance_card = tk.Frame(left_frame, bg=COLOR_CARD_BG, highlightbackground=COLOR_BORDER, highlightthickness=1, relief="flat")
    balance_card.pack(fill="x", padx=20, pady=(10, 20))
    
    balance_label = tk.Label(balance_card, text="Current Balance", font=("Calibri", 11), bg=COLOR_CARD_BG, fg="#555555")
    balance_label.pack(pady=(10, 0))
    
    def update_balance_display():
        current_balance = logic.current_balance()
        balance_value.config(text=f"₱{current_balance:,.2f}")
    
    balance_value = tk.Label(balance_card, text=f"₱{logic.current_balance():,.2f}", font=("Calibri", 18, "bold"), bg=COLOR_CARD_BG, fg=COLOR_SIDEBAR_ACTIVE)
    balance_value.pack(pady=(0, 10))
    
    # Store reference to update balance after actions
    global _balance_value_ref
    _balance_value_ref = balance_value 
    cancel_button.pack_forget()  # hide (only show when edit is pressed)

    # right frame
    right_frame = tk.Frame(split_container, bg=COLOR_CONTENT_BG)
    right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)

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
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

    def handle_card_action(action, target_id):
        if action == "remove":
            response = tk.messagebox.askyesno("Delete", "Are you sure you want to delete?")
            if response:
                logic.remove_target(target_id)  # Call the logic to remove income
                tk.messagebox.showinfo("Success", "Deletion of Target Successful!")
                refresh_cards()  # Refresh the cards to reflect changes
        elif action == "edit": 
            for item in logic.get_savings():
                if item.get_target_id() == target_id:
                    editing_id[0] = target_id
                    page_title.config(text="Edit Target")
                    submit_button.config(text="Update Target")
                    item_input.delete(0, tk.END) # delete input
                    item_input.insert(0, item.get_name()) # insert current data
                    cost_input.delete(0, tk.END)
                    cost_input.insert(0, item.get_cost())
                    target_input.delete(0, tk.END)
                    target_input.insert(0, item.get_date())
                    cancel_button.pack(fill="x", padx=20, pady=(5, 0))
                    break

        elif action == "add_funds":
            fund = tk.simpledialog.askfloat("Add Funds", "Enter amount to add:")
            if fund is None:  # User canceled the dialog
                return
            if fund <= 0:
                tk.messagebox.showwarning("Error", "Amount must be greater than zero.")
                return
            for item in logic.get_savings():
                if item.get_target_id() == target_id:
                    if logic.current_balance() < fund:
                        tk.messagebox.showwarning("Error", "Insufficient balance.")
                        return
                    item.set_saved(item.get_saved() + fund)
                    tk.messagebox.showinfo("Success", f"Added ₱{fund:,.2f} to {item.get_name()}.")
                    refresh_cards()
                    break

        elif action == "minus_funds":
            fund = tk.simpledialog.askfloat("Deduct Funds", "Enter amount to deduct:")
            if fund is None:  # User canceled the dialog
                return
            if fund <= 0:
                tk.messagebox.showwarning("Error", "Amount must be greater than zero.")
                return
            for item in logic.get_savings():
                if item.get_target_id() == target_id:
                    if item.get_saved() < fund:
                        tk.messagebox.showwarning("Error", "Insufficient saved funds.")
                        return
                    item.set_saved(item.get_saved() - fund)
                    tk.messagebox.showinfo("Success", f"Deducted ₱{fund:,.2f} from {item.get_name()}.")
                    refresh_cards()
                    break

    def create_target_card(parent, row, col, target_id, name, cost_str, saved_str, needed_str, progress_val, date):
        # card
        card = tk.Frame(parent, bg=COLOR_CARD_BG, highlightbackground=COLOR_BORDER)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)

        # tiny frame on the top of the card
        top_row = tk.Frame(card, bg=COLOR_CARD_BG)
        top_row.pack(fill="x", padx=10, pady=(10, 5))

        # name
        name_label = tk.Label(top_row, text=name.upper(), font=("Calibri", 10, "bold"), fg="black", bg=COLOR_CARD_BG)
        name_label.pack(side="left")

        # remove button
        remove_button = tk.Button(top_row, text="Remove", font=("Calibri", 10), fg="red", bg=COLOR_CARD_BG, bd=0, cursor="hand2", command=lambda: handle_card_action("remove", target_id))
        remove_button.pack(side="right")

        # edit button
        edit_button = tk.Button(top_row, text="Edit", font=("Calibri", 10), fg="#64748B", bg=COLOR_CARD_BG, bd=0, cursor="hand2", command=lambda: handle_card_action("edit", target_id))
        edit_button.pack(side="right", padx=5)

        # Add Funds button
        add_fund_button = tk.Button(top_row, text="Add Funds", font=("Calibri", 10), fg="green", bg=COLOR_CARD_BG, bd=0, cursor="hand2", command=lambda: handle_card_action("add_funds", target_id))
        add_fund_button.pack(side="right")

        # Deduct Funds button
        minus_fund_button = tk.Button(top_row, text="Deduct Funds", font=("Calibri", 10), fg="green", bg=COLOR_CARD_BG, bd=0, cursor="hand2", command=lambda: handle_card_action("minus_funds", target_id))
        minus_fund_button.pack(side="right")

        # cost
        cost_label = tk.Label(card, text=f"₱{cost_str:,.2f}", font=("Calibri", 20, "bold"), fg="black", bg=COLOR_CARD_BG)
        cost_label.pack(anchor="w", padx=10)

        # description
        saved_label = tk.Label(card, text=f"Saved: ₱{saved_str:,.2f}", font=("Calibri", 12), fg="#555555", bg=COLOR_CARD_BG)
        saved_label.pack(anchor="w", padx=10)

        # description
        needed_label = tk.Label(card, text=f"Needed: ₱{needed_str:,.2f}", font=("Calibri", 12), fg="#555555", bg=COLOR_CARD_BG)
        needed_label.pack(anchor="w", padx=10)

        # progress bar
        progress = ttk.Progressbar(card, style="TProgressbar", orient="horizontal", length=200, mode="determinate")
        progress.pack(fill="x", padx=10, pady=(0, 5))
        progress["value"] = progress_val # Purely visual value passed in

        # goal date
        goal_label = tk.Label(card, text=f"Goal Date: {date}", font=("Calibri", 10), fg="#888888", bg=COLOR_CARD_BG)
        goal_label.pack(anchor="w", padx=10, pady=(5, 15))

    def refresh_cards():
        # Clear all existing savings cards
        for existing_card_widget in target_grid.winfo_children():
            existing_card_widget.destroy()

        update_balance_display()

        # get all the savings data
        current_savings_list = logic.get_savings()

        # Create and display a new card for each income
        card_pos = 0 # starts at 0 each time so it generates at the top
        for savings_index in range(len(current_savings_list) - 1, -1, -1): # reversed
            # get the actual savings item from list using its current index.
            target_savings = current_savings_list[savings_index]

            # 1 card per row
            target_row = card_pos
            target_column = 0

            # call a separate function to visually create one income card.
            create_target_card(parent=target_grid, row=target_row, col=target_column, target_id=target_savings.get_target_id(), name=target_savings.get_name(), cost_str=target_savings.get_cost(), saved_str=target_savings.get_saved(), needed_str=target_savings.get_needed(), progress_val=target_savings.get_progress(), date=target_savings.get_date())
            card_pos += 1

    refresh_cards()