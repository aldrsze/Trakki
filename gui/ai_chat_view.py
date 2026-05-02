import tkinter as tk
from colors import *

# Global reference to store the content box for refreshing
chat_content_box = None
chat_display = None
chat_input = None
message_list = []
chat_initialized = False
chat_greeted = False
ai_chat = None
logic_ref = None

# temp key, for testing only
GROQ_API_KEY = "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"

# view ai chat
def viewai_chat(root, content_box, logic):
    # global variables
    global chat_content_box, chat_initialized, chat_greeted, ai_chat, logic_ref
    chat_content_box = content_box
    logic_ref = logic
    
    # Initialize AI chat once
    if not chat_initialized:
        try:
            from logic.ai_model import AIChat
            ai_chat = AIChat(GROQ_API_KEY)
            if not chat_greeted:
                message_list.append(("AI", "Hi! I'm Penoy, your financial assistant. Ask me about your income, expenses, or savings."))
                chat_greeted = True
            refresh_chat(logic)
            chat_initialized = True
        except Exception as e:
            if not chat_greeted:
                message_list.append(("AI", "Hi! I'm Penoy, your financial assistant. Ask me about your income, expenses, or savings."))
                chat_greeted = True
            refresh_chat(logic)
    else:
        # clear conversation history / ai memory
        if ai_chat:
            ai_chat.conversation_history = []

# refresh_chat
def refresh_chat(logic):
    global chat_content_box, chat_display, chat_input

    for widget in chat_content_box.winfo_children():
        widget.destroy()

    # Main frame
    main_frame = tk.Frame(chat_content_box, bg=COLOR_CONTENT_BG)
    main_frame.pack(fill="both", expand=True, padx=15, pady=15)

    # Chat History Label
    chat_label = tk.Label(main_frame, text="Chat History:", font=("Calibri", 12, "bold"), bg=COLOR_CONTENT_BG)
    chat_label.pack(anchor="w", pady=(0, 8))

    # Chat Display Box
    chat_frame = tk.Frame(main_frame, bg="white", relief="solid", bd=1)
    chat_frame.pack(fill="both", expand=True, pady=(0, 15))

    # char display
    chat_display = tk.Text(
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
    chat_display.pack(fill="both", expand=True)

    display_messages()

    # suggested prompts label
    prompts_label = tk.Label(main_frame, text="Suggested Prompts:", font=("Calibri", 12, "bold"), bg=COLOR_CONTENT_BG)
    prompts_label.pack(anchor="w", pady=(10, 8))

    # suggested prompts container
    prompts_frame = tk.Frame(main_frame, bg=COLOR_CONTENT_BG)
    prompts_frame.pack(fill="x", pady=(0, 15))
    
    # grid columns for horizontal layout
    for i in range(4):
        prompts_frame.grid_columnconfigure(i, weight=1)

    prompt_suggestions = [
        "What is Trakki?",
        "How much have I spent this month?",
        "What's my total savings?",
        "Analyze my spending patterns",
        "Give me a budget recommendation",
        "What are my top expenses?",
        "How can I save more money?",
        "Compare my income vs expenses"
    ]

    def insert_prompt(prompt_text):
        chat_input.delete("1.0", "end")
        chat_input.insert("1.0", prompt_text)
        chat_input.focus()

    # Display prompts in 4 columns (2 rows for 8 items)
    for index, prompt in enumerate(prompt_suggestions):
        row = index // 4
        col = index % 4
        
        # prompt button label
        prompt_btn = tk.Label(
            prompts_frame,
            text=f"• {prompt}",
            font=("Calibri", 11),
            fg=COLOR_PROMPT_LINK,
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

    # Input Row Frame
    input_row = tk.Frame(main_frame, bg=COLOR_CONTENT_BG)
    input_row.pack(fill="both", pady=(0, 10))

    # Input Box
    input_container = tk.Frame(input_row, bg="white", relief="solid", bd=1)
    input_container.pack(side="left", fill="both", expand=True, padx=(0, 8))

    # input text
    chat_input = tk.Text(
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
    chat_input.pack(fill="both", expand=True)
    chat_input.bind("<Control-Return>", lambda e: send_message())

    # send message function
    def send_message():
        global ai_chat, logic_ref
        message = chat_input.get("1.0", "end-1c").strip()
        # if there message is not empty
        if message:
            message_list.append(("You", message))
            chat_input.delete("1.0", "end")
            
            # if ai is ready, get the reply
            if ai_chat and logic_ref:
                try:
                    # send the message to the ai
                    ai_response = ai_chat.chat(message, logic_ref)
                    # save the ai reply
                    message_list.append(("AI", ai_response))
                except Exception as e:
                    # if there is an error, show it in the chat
                    message_list.append(("AI", f"Error: {str(e)}"))
            
            # update the screen so the new messages show up
            display_messages()

    # clear chat function
    def clear_chat():
        global message_list, ai_chat, chat_greeted
        message_list = []
        chat_greeted = False
        if ai_chat:
            ai_chat.clear_history()
        # show the first greeting again after clearing
        message_list.append(("AI", "Hi! I'm Penoy, your financial assistant. Ask me about your income, expenses, or savings."))
        chat_greeted = True
        display_messages()

    # Button Frame
    button_frame = tk.Frame(input_row, bg=COLOR_CONTENT_BG)
    button_frame.pack(side="right", fill="y")
    
    # send button
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

    # clear button
    clear_btn = tk.Button(
        button_frame,
        text="Clear",
        font=("Calibri", 11, "bold"),
        bg=COLOR_DANGER,
        fg="white",
        padx=12,
        pady=6,
        bd=0,
        command=clear_chat
    )
    clear_btn.pack(side="left")

# function for displaying messages
def display_messages():
    global chat_display, message_list
    
    # unlock the text box so it is editable
    chat_display.config(state="normal")
    # remove old messages first
    chat_display.delete("1.0", "end")
    
    # go through each saved message and show it
    for sender, message in message_list:
        if sender == "You":
            # user message style
            chat_display.insert("end", f"YOU:\n", "user_header")
            chat_display.insert("end", f"{message}\n\n", "user_message")
        else:
            # ai message style
            chat_display.insert("end", f"AI:\n", "ai_header")
            chat_display.insert("end", f"{message}\n\n", "ai_message")
    
    # set the colors and font styles
    chat_display.tag_config("user_header", foreground=COLOR_USER_HEADER, font=("Calibri", 15, "bold"))
    chat_display.tag_config("user_message", foreground="black", font=("Calibri", 15))
    chat_display.tag_config("ai_header", foreground=COLOR_AI_HEADER, font=("Calibri", 15, "bold"))
    chat_display.tag_config("ai_message", foreground="black", font=("Calibri", 15))
    
    # lock it again so the user cannot type in it
    chat_display.config(state="disabled")
    # scroll to the latest message
    chat_display.see("end")