import tkinter as tk
import os
from dotenv import load_dotenv
from colors import *

load_dotenv()

# Global reference to store the content box for refreshing
_chat_content_box = None
_chat_display = None
_chat_input = None
_message_list = []
_chat_initialized = False
_ai_chat = None
_logic_ref = None

# securely fetch the api key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def view_ai_chat(root, content_box, logic):
    global _chat_content_box, _chat_initialized, _ai_chat, _logic_ref
    _chat_content_box = content_box
    _logic_ref = logic
    
    # Initialize AI chat once
    if not _chat_initialized:
        try:
            from logic.ai_model import AIChat
            _ai_chat = AIChat(GROQ_API_KEY)
            refresh_chat(logic)
            _chat_initialized = True
        except Exception as e:
            refresh_chat(logic)
    else:
        if _ai_chat:
            _ai_chat.conversation_history = []

def refresh_chat(logic):
    global _chat_content_box, _chat_display, _chat_input

    if _chat_content_box is None:
        return

    for widget in _chat_content_box.winfo_children():
        widget.destroy()

    # Main frame
    main_frame = tk.Frame(_chat_content_box, bg=COLOR_CONTENT_BG)
    main_frame.pack(fill="both", expand=True, padx=15, pady=15)

    # Chat History Label
    chat_label = tk.Label(main_frame, text="Chat History:", font=("Calibri", 12, "bold"), bg=COLOR_CONTENT_BG)
    chat_label.pack(anchor="w", pady=(0, 8))

    # Chat Display Box
    chat_frame = tk.Frame(main_frame, bg="white", relief="solid", bd=1)
    chat_frame.pack(fill="both", expand=True, pady=(0, 15))

    _chat_display = tk.Text(
        chat_frame,
        height=10,
        width=120,
        bg="white",
        fg="black",
        font=("Calibri", 13),
        wrap="word",
        state="disabled",
        relief="flat",
        bd=0,
        padx=10,
        pady=10
    )
    _chat_display.pack(fill="both", expand=True)

    display_messages()

    # Suggested Prompts Label
    prompts_label = tk.Label(main_frame, text="Suggested Prompts:", font=("Calibri", 12, "bold"), bg=COLOR_CONTENT_BG)
    prompts_label.pack(anchor="w", pady=(10, 8))

    # Suggested Prompts Container
    prompts_frame = tk.Frame(main_frame, bg=COLOR_CONTENT_BG)
    prompts_frame.pack(fill="x", pady=(0, 15))
    
    # Configure grid columns for horizontal layout
    for i in range(4):
        prompts_frame.grid_columnconfigure(i, weight=1)

    prompt_suggestions = [
        "How much have I spent this month?",
        "What's my total savings?",
        "Analyze my spending patterns",
        "Give me a budget recommendation",
        "What are my top expenses?",
        "How can I save more money?",
        "Compare my income vs expenses"
    ]

    def insert_prompt(prompt_text):
        _chat_input.delete("1.0", "end")
        _chat_input.insert("1.0", prompt_text)
        _chat_input.focus()

    # Display prompts in 4 columns (2 rows for 7 items)
    for idx, prompt in enumerate(prompt_suggestions):
        row = idx // 4
        col = idx % 4
        
        prompt_btn = tk.Label(
            prompts_frame,
            text=f"• {prompt}",
            font=("Calibri", 11),
            fg="#2563EB",
            bg=COLOR_CONTENT_BG,
            cursor="hand2",
            wraplength=280,
            justify="left"
        )
        prompt_btn.grid(row=row, column=col, sticky="w", padx=5, pady=3)
        prompt_btn.bind("<Button-1>", lambda e, p=prompt: insert_prompt(p))

    # Your Message Label
    input_label = tk.Label(main_frame, text="Your message:", font=("Calibri", 12, "bold"), bg=COLOR_CONTENT_BG)
    input_label.pack(anchor="w", pady=(10, 8))

    # Input Row (Input Box + Buttons)
    input_row = tk.Frame(main_frame, bg=COLOR_CONTENT_BG)
    input_row.pack(fill="both", pady=(0, 10))

    # Input Box
    input_container = tk.Frame(input_row, bg="white", relief="solid", bd=1)
    input_container.pack(side="left", fill="both", expand=True, padx=(0, 8))

    _chat_input = tk.Text(
        input_container,
        height=3,
        width=100,
        bg="white",
        fg="black",
        font=("Calibri", 13),
        wrap="word",
        relief="flat",
        bd=0,
        padx=10,
        pady=10
    )
    _chat_input.pack(fill="both", expand=True)
    _chat_input.bind("<Control-Return>", lambda e: send_message())

    def send_message():
        global _ai_chat, _logic_ref
        message = _chat_input.get("1.0", "end-1c").strip()
        if message:
            _message_list.append(("You", message))
            _chat_input.delete("1.0", "end")
            
            if _ai_chat and _logic_ref:
                try:
                    ai_response = _ai_chat.chat(message, _logic_ref)
                    _message_list.append(("AI", ai_response))
                except Exception as e:
                    _message_list.append(("AI", f"Error: {str(e)}"))
            
            display_messages()

    def clear_chat():
        global _message_list, _ai_chat
        _message_list = []
        if _ai_chat:
            _ai_chat.clear_history()
        display_messages()

    # Button Frame
    button_frame = tk.Frame(input_row, bg=COLOR_CONTENT_BG)
    button_frame.pack(side="right", fill="y")

    send_btn = tk.Button(
        button_frame,
        text="Send",
        font=("Calibri", 11, "bold"),
        bg=COLOR_SIDEBAR,
        fg="white",
        padx=12,
        pady=6,
        bd=0,
        command=send_message
    )
    send_btn.pack(side="left", padx=(0, 5))

    clear_btn = tk.Button(
        button_frame,
        text="Clear",
        font=("Calibri", 11, "bold"),
        bg="#EF4444",
        fg="white",
        padx=12,
        pady=6,
        bd=0,
        command=clear_chat
    )
    clear_btn.pack(side="left")

def display_messages():
    global _chat_display, _message_list
    
    if _chat_display is None:
        return
    
    _chat_display.config(state="normal")
    _chat_display.delete("1.0", "end")
    
    for sender, message in _message_list:
        if sender == "You":
            _chat_display.insert("end", f"YOU:\n", "user_header")
            _chat_display.insert("end", f"{message}\n\n", "user_message")
        else:
            _chat_display.insert("end", f"AI:\n", "ai_header")
            _chat_display.insert("end", f"{message}\n\n", "ai_message")
    
    _chat_display.tag_config("user_header", foreground="#3498db", font=("Calibri", 15, "bold"))
    _chat_display.tag_config("user_message", foreground="black", font=("Calibri", 15))
    _chat_display.tag_config("ai_header", foreground="#2ecc71", font=("Calibri", 15, "bold"))
    _chat_display.tag_config("ai_message", foreground="black", font=("Calibri", 15))
    
    _chat_display.config(state="disabled")
    _chat_display.see("end")