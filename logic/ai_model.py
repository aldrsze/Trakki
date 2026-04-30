try:
    import requests
except ImportError:
    raise ImportError("requests package required. pip install requests --target ./lib")

class AIChat:
    def __init__(self, api_key):
        """Initialize AI chat with Groq API (Free & Fast)"""
        if not api_key or api_key == "YOUR_GROQ_API_KEY":
            raise ValueError(
                "Please set a valid GROQ_API_KEY in gui/ai_chat_view.py. "
                "Get your free API key from: https://console.groq.com"
            )
        
        self.api_key = api_key
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.conversation_history = []
    
    def get_financial_summary(self, logic):
        # Extract full financial data from the logic controller.
        # means the ai has full access to all of the data
        incomes = logic.get_incomes()
        expenses = logic.get_expenses()
        savings = logic.get_savings()

        total_income = 0
        for income in incomes:
            total_income += income.get_amount()

        total_expenses = 0
        for expense in expenses:
            total_expenses += expense.get_amount()

        total_saved = 0
        for goal in savings:
            total_saved += goal.get_saved()

        current_balance = logic.current_balance()

        summary = f"""
FINANCIAL DATA SUMMARY:
- Total Income: ₱{total_income:,.2f}
- Total Expenses: ₱{total_expenses:,.2f}
- Total Saved: ₱{total_saved:,.2f}
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
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            
            # Prepare messages for Groq API
            messages = [
                {"role": "system", "content": system_prompt},
            ]
            
            # Add conversation history (last 5 messages for context)
            for msg in self.conversation_history[-5:]:
                messages.append(msg)
            
            payload = {
                "model": "llama-3.1-8b-instant",  # Free model
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1024,
            }
            
            response = requests.post(self.api_url, json=payload, headers=headers, timeout=15)
            
            if response.status_code != 200:
                try:
                    error_data = response.json()
                    error_msg = error_data.get("error", {}).get("message", f"HTTP {response.status_code}")
                except:
                    error_msg = f"HTTP {response.status_code}"
                raise Exception(f"API Error: {error_msg}")
            
            result = response.json()
            ai_response = result["choices"][0]["message"]["content"].strip()
            
            # Add AI response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_response
            })
            
            return ai_response
        except requests.exceptions.Timeout:
            return "Request timed out. Please try again."
        except requests.exceptions.ConnectionError:
            return "Connection error. Please check your internet connection."
        except Exception as e:
            return f"Error: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
