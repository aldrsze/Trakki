import tkinter as tk
from PIL import Image, ImageTk
from colors import *

from gui import income_view
from gui import expenses_view
from gui import targets_view
from gui import dashboard_view
from gui import table_view
from gui import ai_chat_view

from logic.controller import TrakkiLogic

app_logic = TrakkiLogic()

# Show all data in terminal for dashboard calculations
print("All Incomes:", app_logic.get_incomes())
print("All Expenses:", app_logic.get_expenses())
print("All Targets:", app_logic.get_targets())

# For each income, expense, and target, print details
for income in app_logic.get_incomes():
    print("Income:", income.get_amount(), income.get_category(), income.get_desc())

for expense in app_logic.get_expenses():
    print("Expense:", expense.get_amount(), expense.get_category(), expense.get_desc())

for target in app_logic.get_targets():
    print("Target:", target.get_name(), target.get_cost(), target.get_date(), target.get_saved(), target)

# root window
root = tk.Tk()
root.title("Trakki")
root.geometry("1300x800") # dimensions
root.resizable(False, False) # non-resizable
root.configure(bg=COLOR_MAIN_BG)

# sidebar
sidebar = tk.Frame(
    root, bg=COLOR_SIDEBAR,
    highlightbackground='black',
    highlightthickness=1,
    bd=0,
    width=200
)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False) # Makes the sidebar fixed dimension

# main area
main_area = tk.Frame(
    root,
    bg=COLOR_MAIN_BG, # Changed to COLOR_MAIN_BG, as active sidebar color is only for button
    highlightbackground='black',
    highlightthickness=1,
    bd=0,
)
main_area.pack(side="left", fill="both", expand=True)

app_name = tk.Label(
    sidebar,
    text="TRAKKI",
    font=("Roboto", 30, "bold"),
    bg=COLOR_SIDEBAR,
    fg="white",
)
app_name.pack(pady=(30, 50))

# stacks the page on top of each other
main_area.grid_rowconfigure(0, weight=1)
main_area.grid_columnconfigure(0, weight=1)

# Dictionary to store the main Frame for each page (which will contain all its widgets)
pages = {}
# Dictionary to store navigation buttons
nav_buttons = {}

# FUNCTIONS 
def show_page(page_name):
    # Update navigation button styles
    for name in nav_buttons:
        if name == page_name:
            nav_buttons[name].configure(bg=COLOR_SIDEBAR_ACTIVE) # Changes the color if active
        else:
            nav_buttons[name].configure(bg=COLOR_SIDEBAR)

    if page_name == "Dashboard":
        dashboard_view.refresh_dashboard(app_logic)

    # Bring the selected page's frame to the front
    page_to_open = pages[page_name]
    page_to_open.tkraise()

nav_items = [
    ("Dashboard", dashboard_view.view_dashboard),
    ("Income", income_view.view_income),
    ("Expenses", expenses_view.view_expenses),
    ("Targets", targets_view.view_targets),
    ("Table View", table_view.view_table ), 
    ("AI Chat",  ai_chat_view.view_ai_chat) 
]

# Create all pages and their contents at startup
for item_name, builder_func in nav_items:
    # top-level frame for this page within the main_area
    page_frame = tk.Frame(main_area, bg=COLOR_MAIN_BG)
    page_frame.grid(row=0, column=0, sticky="nsew")
    pages[item_name] = page_frame # Store this frame for show_page to access

    # title label
    title_label = tk.Label(
        page_frame,
        text= f"- {item_name.upper()} -",
        font="Calibri 24 bold",
        bg=COLOR_MAIN_BG,
        fg="black"
    )
    title_label.pack(anchor="n", padx=30)

    # content_box for the specific page
    content_box = tk.Frame(
        page_frame, # parent is the page_frame
        bg=COLOR_CONTENT_BG,
        highlightbackground=COLOR_BORDER,
        highlightthickness=0
    )
    content_box.pack(fill="both", expand=True, padx=40)

    builder_func(root, content_box, app_logic)

    # navigation button for this page
    btn = tk.Button(
        sidebar,
        text=item_name,
        font="Calibri 16", # font
        bg=COLOR_SIDEBAR, # background
        fg="white", # foreground
        anchor="w", # left aligned text
        bd=0, # border width
        padx=20,
        pady=10,
        cursor="hand2",
        command=lambda name=item_name: show_page(name) # a way to put a function with parameter in a button 
    )
    btn.pack(fill="x", pady=1)
    nav_buttons[item_name] = btn 

# Logo
original_logo = Image.open("res/TrakkiLogo.png") 
new_width = 140
logo_aspect_ratio = original_logo.height / original_logo.width
new_height = int(new_width * logo_aspect_ratio)

# convert it into a TK image
resized_logo = original_logo.resize((new_width, new_height))
logo_img = ImageTk.PhotoImage(resized_logo)

# put the image in a label
logo_label = tk.Label(sidebar, image=logo_img, bg=COLOR_SIDEBAR)
logo_label.image = logo_img 
logo_label.pack(pady=(80, 20))

# dev name
dev_name = tk.Label(
    sidebar,
    text="aldrsze.",
    font=("Roboto", 12),
    bg=COLOR_SIDEBAR,
    fg="white",
)
dev_name.pack(pady=10)

# shows the page of dashboard first
show_page("Dashboard")

root.mainloop()



