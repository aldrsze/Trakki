import tkinter as tk
from tkinter import ttk
from datetime import datetime
from colors import *

# Global reference to store the content box for refreshing
_table_content_box = None

def view_table(root, content_box, logic):
    global _table_content_box
    _table_content_box = content_box

    # Refresh the table every time the view is activated
    refresh_table(logic)

def refresh_table(logic):
    global _table_content_box

    if _table_content_box is None:
        return

    # Clear everything 
    all_widgets = _table_content_box.winfo_children()
    for w in all_widgets:
        w.destroy()

    # Main frame for the view table
    main_frame = tk.Frame(_table_content_box, bg=COLOR_CONTENT_BG)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Header frame
    header_frame = tk.Frame(main_frame, bg=COLOR_CONTENT_BG)
    header_frame.pack(fill="x", pady=(10, 20), padx=20)

    # Title label
    page_title = tk.Label(
        header_frame,
        text="All Transactions History",
        font=("Calibri", 20, "bold"),
        bg=COLOR_CONTENT_BG
    )
    page_title.pack(side="left")

    # Setup Treeview (Table) first
    tree_frame = tk.Frame(main_frame, bg=COLOR_CONTENT_BG, highlightbackground=COLOR_BORDER, highlightthickness=1)
    tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    tree_scroll = ttk.Scrollbar(tree_frame)
    tree_scroll.pack(side="right", fill="y")

    columns = ("Type", "Category/Name", "Description", "Amount/Cost", "Date")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=tree_scroll.set, selectmode="extended")
    tree.pack(fill="both", expand=True)
    tree_scroll.config(command=tree.yview)

    # Headings
    tree.heading("Type", text="Type", anchor="w")
    tree.heading("Category/Name", text="Category/Name", anchor="w")
    tree.heading("Description", text="Description", anchor="w")
    tree.heading("Amount/Cost", text="Amount/Cost", anchor="w")
    tree.heading("Date", text="Date", anchor="w")

    # Column widths
    tree.column("Type", width=120, anchor="w")
    tree.column("Category/Name", width=180, anchor="w")
    tree.column("Description", width=300, anchor="w")
    tree.column("Amount/Cost", width=150, anchor="w")
    tree.column("Date", width=150, anchor="w")

    # Style the treeview (table)
    style = ttk.Style()
    style.theme_use("default")
    style.configure(
        "Treeview", 
        background=COLOR_CARD_BG,
        foreground="black",
        rowheight=35,
        fieldbackground=COLOR_CARD_BG,
        font=("Calibri", 12),
        borderwidth=0
    )
    style.map('Treeview', background=[('selected', COLOR_SIDEBAR_ACTIVE)])
    style.configure(
        "Treeview.Heading", 
        font=("Calibri", 13, "bold"),
        background=COLOR_BORDER,
        foreground="black",
        borderwidth=0
    )

    # Sorting and Updating Logic
    def parse_date(d):
        try:
            return datetime.strptime(str(d).strip(), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                return datetime.strptime(str(d).strip(), "%Y-%m-%d")
            except ValueError:
                return datetime.min

    def update_the_table():
        # Delete old rows
        for r in tree.get_children():
            tree.delete(r)

        my_data_list = []

        # gets all the data
        for i in logic.get_incomes():
            my_data_list.append(("Income", i.get_category(), i.get_desc(), i.get_amount(), i.get_date()))
            
        for e in logic.get_expenses():
            my_data_list.append(("Expense", e.get_category(), e.get_desc(), e.get_amount(), e.get_date()))
            
        for transaction in logic.get_savings_transactions():
            my_data_list.append(("Target Savings", transaction.get_target_name(), "Savings Deposit", transaction.get_amount(), transaction.get_date()))

        # Sort based on date and time (newly added on top)
        my_data_list.sort(key=lambda x: parse_date(x[4]), reverse=True)

        # Loop through the sorted list and put them in the treeview
        for item in my_data_list:
            type_of_record = item[0]
            name = item[1]
            description = item[2]
            money = float(item[3])
            date = item[4]
            
            if type_of_record == "Expense" or type_of_record == "Target Savings":
                sign = "-"
            else:
                sign = ""
            money_string = sign + "₱" + "{:,.2f}".format(money)
            
            # Put the row in the table
            tree.insert("", "end", values=(type_of_record, name, description, money_string, date))

    # run
    update_the_table()