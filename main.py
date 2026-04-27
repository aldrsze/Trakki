import tkinter as tk
from PIL import Image, ImageTk
from colors import *

from gui import income_view
from gui import expenses_view
from gui import targets_view

from logic.controller import TrakkiLogic

app_logic = TrakkiLogic()

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
    bg=COLOR_SIDEBAR_ACTIVE,
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

pages = {}
nav_buttons = {}

# FUNCTIONS 
def show_page(page_name):
    for name in nav_buttons:
        if name == page_name:
            nav_buttons[name].configure(bg=COLOR_SIDEBAR_ACTIVE) # Changes the color if active
        else:
            nav_buttons[name].configure(bg=COLOR_SIDEBAR)

    page_to_open = pages[page_name]
    page_to_open.tkraise() # bring the page to front

# navigation items
nav_items = ["Dashboard", "Income", "Expenses", "Targets", "Table View", "AI Chat"]

# I used a loop so it doesnt repeat the same code
for item in nav_items:
    btn = tk.Button(
        sidebar,
        text=item,
        font="Calibri 16", # font
        bg=COLOR_SIDEBAR, # background
        fg="white", # foreground
        anchor="w", # left aligned text
        bd=0, # border width
        padx=20,
        pady=10,
        cursor="hand2",
        command=lambda name=item: show_page(name) # a way to put a function with parameter in a button 
    )
    btn.pack(fill="x", pady=1)
    nav_buttons[item] = btn # put it in a dictionary i made

    # Page frame
    page_frame = tk.Frame(main_area, bg=COLOR_MAIN_BG)
    page_frame.grid(row=0, column=0, sticky="nsew")
    pages[item] = page_frame # store it in a dict also

    title_label = tk.Label(
        page_frame,
        text= f"- {item.upper()} -",
        font="Calibri 24 bold",
        bg=COLOR_MAIN_BG,
        fg="black"
    )
    title_label.pack(anchor="n", padx=30, pady=(30, 10))

    content_box = tk.Frame(
        page_frame,
        bg=COLOR_CONTENT_BG,
        highlightbackground=COLOR_BORDER,
        highlightthickness=0
    )
    content_box.pack(fill="both", expand=True, padx=40, pady=(0, 30))

    # conditions on which file/module will run
    if item == "Dashboard": pass
    elif item == "Income": income_view.view_income(root, content_box, app_logic) 
    elif item == "Expenses": expenses_view.view_expenses(root, content_box, app_logic)
    elif item == "Targets": targets_view.view_targets(root, content_box, app_logic)
    elif item == "Table View": pass
    elif item == "AI Chat": pass

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



