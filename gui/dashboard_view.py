import tkinter as tk
from colors import *

def view_dashboard(root, content_box, logic):

    main_frame = tk.Frame(content_box, bg=COLOR_CONTENT_BG)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    page_title = tk.Label(
            main_frame,
            text="dashboard",
            font=("Calibri", 20, "bold"),
            bg = COLOR_CONTENT_BG
        )
    page_title.pack(pady=20, anchor="w", padx=20)