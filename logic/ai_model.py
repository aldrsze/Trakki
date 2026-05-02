try:
    import requests
except ImportError:
    raise ImportError("requests package required. pip install requests")

class AIChat:
    def __init__(self, api_key):
        # Initialize AI chat with Groq API
        if not api_key or api_key == "YOUR_GROQ_API_KEY":
            raise ValueError("API NOT VALID")
        
        self.api_key = api_key
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.conversation_history = []
    
    def get_financial_summary(self, logic):
        # Extract full financial data from the logic controller.
        # means the ai has full access to all of the data
        incomes = logic.get_incomes()
        expenses = logic.get_expenses()
        savings = logic.get_savings()

        total_income = logic.total_income()
        total_expenses = logic.total_expenses()
        total_savings = logic.total_savings()
        current_balance = logic.current_balance()

        summary = f"""
FINANCIAL DATA SUMMARY:
- Total Income: ₱{total_income:,.2f}
- Total Expenses: ₱{total_expenses:,.2f}
- Total Saved: ₱{total_savings:,.2f}
- Current Balance: ₱{current_balance:,.2f}

INCOMES:
"""
        for income in incomes:
            summary += (
                f"  • Income ID: {income.get_income_id()}\n"
                f"    Amount: ₱{income.get_amount():,.2f}\n"
                f"    Category: {income.get_category()}\n"
                f"    Description: {income.get_desc()}\n"
                f"    Date: {income.get_date()}\n"
            )

        summary += "\nEXPENSES:\n"
        for expense in expenses:
            summary += (
                f"  • Expense ID: {expense.get_expense_id()}\n"
                f"    Amount: ₱{expense.get_amount():,.2f}\n"
                f"    Category: {expense.get_category()}\n"
                f"    Description: {expense.get_desc()}\n"
                f"    Date: {expense.get_date()}\n"
            )

        summary += "\nSAVINGS GOALS:\n"
        for goal in savings:
            summary += (
                f"  • Target ID: {goal.get_target_id()}\n"
                f"    Name: {goal.get_name()}\n"
                f"    Cost: ₱{goal.get_cost():,.2f}\n"
                f"    Saved: ₱{goal.get_saved():,.2f}\n"
                f"    Needed: ₱{goal.get_needed():,.2f}\n"
                f"    Progress: {goal.get_progress():.1f}%\n"
                f"    Goal Date: {goal.get_date()}\n"
                f"    Created At: {goal.get_created_at()}\n"
            )

        return summary
    
    def chat(self, user_message, logic):
        """Send a message and get AI response from Groq"""
        # Get updated financial summary
        financial_summary = self.get_financial_summary(logic)
        
        # Build the system prompt
        system_prompt = f"""You are the AI Financial Coach named "burat" for "Trakki", a personal finance tracking app. Your goal is to guide, motivate, and advise the user on their financial journey.
    
Here is the user's current financial data:
{financial_summary}

ROLE & TONE:
- Act like a supportive, financially-savvy friend or mentor.
- Be approachable, empathetic, and strictly non-judgmental.
- Use natural, modern English.

RULES FOR USING THE DATA:
- When user wants you to provide recent data, you must base on the date.
- Base every answer strictly on the provided financial summary.
- Do not invent, assume, or guess any values.
- Dates are very important. Use them to determine recency, ordering, and trends.
- When the user asks for the latest, recent, newest, or most recent income, expense, or savings goal, always choose the item with the newest date in the summary.
- Do not infer recency from amount, category, or description.
- If multiple items exist, compare their date fields carefully and use the newest one.
- When reporting a date and time, format it in a user-friendly form such as "April 07, 2026" or "10:00 PM, April 07, 2026".
- If the user asks for details of a specific item, include all available attributes for that item.

YOUR TASK:
- Analyze the user's financial data and provide highly personalized, actionable advice.
- If they are hitting savings goals or keeping expenses low, give positive reinforcement.
- If their expenses are dangerously close to or exceeding their income, give a gentle, practical warning and a quick tip to adjust.
- If the user asks about a recent item, answer with the exact matching item from the newest date, then give its details.

STRICT CONSTRAINTS:
1. LANGUAGE: Respond ONLY in English.
2. LENGTH: Keep responses concise and easy to read, usually 1-2 paragraphs.
3. SCOPE: Never invent data. Use only the financial summary provided above.
"""
        # Add user message to history list
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            # Create the headers dictionary (needed for the API request)
            # This tells the API server what kind of data we're sending
            headers = {
                # Add the API key for authentication (so the API knows)
                "Authorization": f"Bearer {self.api_key}",
                # Tell the API we're sending JSON format data
                "Content-Type": "application/json",
            }
            
            # Create a list to hold all the messages we want to send to the AI
            # Start with the system prompt that tells the AI how to behave
            messages = [
                {"role": "system", "content": system_prompt},
            ]
            
            # Loop through the last 5 messages from our conversation history
            # This gives the AI context about what we've been talking about
            for msg in self.conversation_history[-5:]:
                # Add each message to our messages list
                messages.append(msg)
            
            # Create the payload (the data packet we're sending to the API)
            # This contains all the info the API needs to generate a response
            payload = {
                # Which AI model to use (llama-3.1-8b-instant is free and fast)
                "model": "llama-3.1-8b-instant",
                "messages": messages,
                # how creative/random the response should be (0.7 is balanced)
                "temperature": 0.7,
                # Max tokens: maximum length of the AI response (512 is reasonable)
                "max_tokens": 512,
            }
            
            # Send a POST request to the Groq API with our payload and headers
            # timeout=15 means if the request takes more than 15 seconds, cancel it
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=15)
            
            # Check if the status code is not 200 (200 means success)
            if response.status_code != 200:
                # Something went wrong with the API request
                # Raise an error with the status code
                raise Exception(f"API Error: HTTP {response.status_code}")
            
            # Convert the API response to JSON format
            result = response.json()
            # Extract the actual AI response text from deep inside the JSON structure
            # [choices][0][message][content] is where the AI's answer is stored
            ai_response = result["choices"][0]["message"]["content"].strip()
            
            # Add the AI's response to our conversation history
            self.conversation_history.append({
                # Mark this as coming from the AI assistant
                "role": "assistant",
                # Store the actual response content
                "content": ai_response
            })
            
            # Return the AI response back to whoever called this function
            return ai_response
        
        # Handle different types of errors that might occur:
        except requests.exceptions.Timeout:
            # If the API request times out (takes too long), return this message
            return "Request timed out. Please try again."
        except requests.exceptions.ConnectionError:
            # If we can't connect to the API (no internet?), return this message
            return "Connection error. Please check your internet connection."
        except Exception as e:
            # For any other error we didn't anticipate, return the error details
            return f"Error: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
