import tkinter as tk
from tkinter import ttk, messagebox
from colors import *

_view_expenses_content_box = None

def view_expenses(root, content_box, logic):
    global _view_expenses_content_box
    _view_expenses_content_box = content_box

    refresh_expense(logic)

def refresh_expense(logic):
    global _view_expenses_content_box

    if _view_expenses_content_box is None:
        return
    
    for widget in _view_expenses_content_box.winfo_children():
        widget.destroy()

    # container
    split_container = tk.Frame(_view_expenses_content_box, bg=COLOR_CONTENT_BG)
    split_container.pack(fill="both", expand=True, padx=10, pady=10)

    # divide the container into two (column 0 and 1)
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

    # Total Expenses Card
    total_expenses_card = tk.Frame(left_frame, bg=COLOR_CARD_BG, highlightbackground=COLOR_BORDER, highlightthickness=1, relief="flat")
    total_expenses_card.pack(fill="x", padx=20, pady=(10, 20))
    
    balance_label = tk.Label(total_expenses_card, text="Total Expenses", font=("Calibri", 11), bg=COLOR_CARD_BG, fg="#555555")
    balance_label.pack(pady=(10, 0))
    
    balance_value = tk.Label(total_expenses_card, text=f"₱{logic.total_expenses():,.2f}", font=("Calibri", 18, "bold"), bg=COLOR_CARD_BG, fg=COLOR_SIDEBAR_ACTIVE)
    balance_value.pack(pady=(0, 10))

    def update_expenses_display():
        total_expenses = logic.total_expenses()
        balance_value.config(text=f"₱{total_expenses:,.2f}")

    # page title
    page_title = tk.Label(left_frame, text="Add New Expense", font=("Calibri", 18, "bold"), bg=COLOR_CONTENT_BG)
    page_title.pack(pady=20, anchor="w", padx=20)

    # Amount input Field
    amount_label = tk.Label(left_frame, text="Amount:", bg=COLOR_CONTENT_BG, font=("Calibri", 14, "bold"))
    amount_label.pack(anchor="w", padx=20)
    amount_input = tk.Entry(left_frame, **input_style)
    amount_input.pack(fill="x", padx=20, pady=(0, 15), ipady=2)

    # category input field
    category_label = tk.Label(left_frame, text="Category:", bg=COLOR_CONTENT_BG, font=("Calibri", 14, "bold"))
    category_label.pack(anchor="w", padx=20)
    category_input = tk.Entry(left_frame, **input_style)
    category_input.pack(fill="x", padx=20, pady=(0, 15), ipady=2)

    # descrioption input field
    description_label = tk.Label(left_frame, text="Description:", bg=COLOR_CONTENT_BG, font=("Calibri", 14, "bold"))
    description_label.pack(anchor="w", padx=20)
    description_input = tk.Text(left_frame, height=6, wrap="word", **input_style)
    description_input.pack(fill="x", padx=20, pady=(0, 10))

    # function for clearing input fields
    def clear_fields():
        amount_input.delete(0, tk.END)
        category_input.delete(0, tk.END)
        description_input.delete('1.0', tk.END)

    def reset_form():
        clear_fields()
        editing_id[0] = None
        page_title.config(text="Add New Expense")
        submit_button.config(text="Add Expense")
        cancel_button.pack_forget()  # Hide the cancel button

    editing_id = [None]

    def handle_submit():
        amount = amount_input.get()
        category = category_input.get()
        desc = description_input.get("1.0", "end-1c")

        # Checks if all fields are not empty
        if not amount or not category:
            tk.messagebox.showwarning("Error", "All Fields are required.")
            return
        # catches unvalid number
        try:
            amount = float(amount)
        except ValueError:
            tk.messagebox.showwarning("Error", "Amount must be a number.")
            return

        total_balance = logic.current_balance()

        if editing_id[0]:
            # Find the existing expense object (if any)
            old_expense = None
            for e in logic.get_expenses():
                if e.get_expense_id() == editing_id[0]:
                    old_expense = e
                    break

            # if there is an existing expense amt, it goes back to the balance
            if old_expense is not None:
                old_amount = float(str(old_expense.get_amount()))
                available_balance = total_balance + old_amount
            # if not, it returns the balance itself
            else:
                available_balance = total_balance

            if amount > available_balance:
                tk.messagebox.showwarning(
                    "Insufficient Balance",
                    f"Your updated expense of ₱{amount:,.2f} exceeds your available balance of ₱{available_balance:,.2f}.\n\nExpense was not updated."
                )
                reset_form()
                return
            # if amount is lower than balance, it updates
            logic.update_expense(editing_id[0], amount, category, desc)
            tk.messagebox.showinfo("Success", "Update Expense Successful!")
        else:
            # For new expenses
            current_balance = total_balance

            if amount > current_balance:
                tk.messagebox.showwarning(
                    "Insufficient Balance",
                    f"Your expense of ₱{amount:,.2f} exceeds your current balance of ₱{current_balance:,.2f}.\n\nExpense was not added."
                )
                reset_form()
                return

            # if amount is lower than current_balance
            logic.add_expense(amount, category, desc)
            tk.messagebox.showinfo("Success", "Add expense Successful!")

        refresh_cards()
        reset_form()

    # Pack the submit button
    submit_button = tk.Button(left_frame, text="Add Expense", bg=COLOR_SIDEBAR, font=("Calibri", 14, "bold"), fg="white", bd=0, padx=15, pady=8, command=handle_submit)
    submit_button.pack(fill="x", padx=20, pady=(10, 5)) 

    # Pack the cancel button
    cancel_button = tk.Button(left_frame, text="Cancel", bg="#EF4444", font=("Calibri", 14, "bold"), fg="white", bd=0, padx=15, pady=8, command=reset_form)
    cancel_button.pack(fill="x", padx=20, pady=(0, 10)) 
    cancel_button.pack_forget()  # hide (only show when edit is pressed)

    # right frame
    right_frame = tk.Frame(split_container, bg=COLOR_CONTENT_BG)
    right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)

    # Canvas - frame that can move up and down
    canvas = tk.Canvas(right_frame, bg=COLOR_CONTENT_BG, highlightthickness=0)

    # scrollbar for the canvas
    scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=canvas.yview)

    # Frame for the cards in the canvas
    expense_grid = tk.Frame(canvas, bg=COLOR_CONTENT_BG)

    # determines how long the list for the scrolling
    expense_grid.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # put frame inside canvas window
    canvas_window = canvas.create_window((0, 0), window=expense_grid, anchor="nw")

    # link scrollbar and canvas
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

    def handle_card_action(action, expense_id):
        if action == "remove":
            response = tk.messagebox.askyesno("Delete", "Are you sure you want to delete?")
            if response:
                logic.remove_expense(expense_id)  # Call the logic to remove income
                tk.messagebox.showinfo("Success", "Deletion of Expense Successful!")
                refresh_cards()  # Refresh the cards to reflect changes
        elif action == "edit": 
            for item in logic.get_expenses():
                if item.get_expense_id() == expense_id:
                    editing_id[0] = expense_id
                    page_title.config(text="Edit Expense")
                    submit_button.config(text="Update Expense")
                    amount_input.delete(0, tk.END) # delete input
                    amount_input.insert(0, item.get_amount()) # insert current data
                    category_input.delete(0, tk.END)
                    category_input.insert(0, item.get_category())
                    description_input.delete('1.0', tk.END)
                    description_input.insert('1.0', item.get_desc())
                    cancel_button.pack(fill="x", padx=20, pady=(5, 0))
                    break

    def create_expense_card(parent, row, col, expense_id, amount, category, desc, date):
        # card
        card = tk.Frame(parent, bg=COLOR_CARD_BG, highlightbackground=COLOR_BORDER)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1)

        # tiny frame on the top of the card
        top_row = tk.Frame(card, bg=COLOR_CARD_BG)
        top_row.pack(fill="x", padx=10, pady=(10, 5))

        # category
        c_label = tk.Label(top_row, text=category.upper(), font=("Calibri", 9, "bold"), fg="red", bg=COLOR_CARD_BG)
        c_label.pack(side="left")

        # remove button
        t_button = tk.Button(top_row, text="Remove", font=("Calibri", 10), fg="#EF4444", bg=COLOR_CARD_BG, bd=0, cursor="hand2", command=lambda: handle_card_action("remove", expense_id))
        t_button.pack(side="right")

        # Edit button
        e_button = tk.Button(top_row, text="Edit", font=("Calibri", 10), fg="#64748B", bg=COLOR_CARD_BG, bd=0, cursor="hand2", command=lambda: handle_card_action("edit", expense_id))
        e_button.pack(side="right", padx=5)

        # Card Details
        amount_details = tk.Label(card, text=f"-₱{float(str(amount)):,.2f}", font=("Calibri", 20, "bold"), fg="black", bg=COLOR_CARD_BG)
        amount_details.pack(anchor="w", padx=10)

        desc_details = tk.Label(card, text=desc, font=("Calibri", 12), fg="#333333", bg=COLOR_CARD_BG, justify="left", wraplength=200)
        desc_details.pack(anchor="w", padx=10, pady=(5, 0))

        date_details = tk.Label(card, text=date, font=("Calibri", 10), fg="#888888", bg=COLOR_CARD_BG)
        date_details.pack(anchor="w", padx=10, pady=(10, 15))

    def refresh_cards():
        # Clear all existing income cards
        for existing_card_widget in expense_grid.winfo_children():
            existing_card_widget.destroy()

        # get all the incomes data
        current_expenses_list = logic.get_expenses()

        update_expenses_display()

        # Create and display a new card for each income
        card_pos = 0 # starts at 0 each time so it generates at the top

        for expense_index in range(len(current_expenses_list) - 1, -1, -1): # reversed
            # get the actual income item from list using its current index.
            expense_item = current_expenses_list[expense_index]

            # calculate which row this card should go into.
            target_row = card_pos // 2

            # Calculate which column this card should go into.
            target_column = card_pos % 2 # Modulo 2 gives remainder (0 or 1)

            # call a separate function to visually create one income card.
            create_expense_card(parent=expense_grid, row=target_row, col=target_column, expense_id=expense_item.get_expense_id(), amount=expense_item.get_amount(), category=expense_item.get_category(), desc=expense_item.get_desc(), date=expense_item.get_date())

            card_pos += 1

    refresh_cards()