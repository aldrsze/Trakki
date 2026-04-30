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
        """Extract financial data from the logic controller"""
        incomes = logic.get_incomes()
        expenses = logic.get_expenses()
        savings = logic.get_savings()
        
        total_income = sum(i.get_amount() for i in incomes)
        total_expenses = sum(e.get_amount() for e in expenses)
        total_saved = sum(s.get_saved() for s in savings)
        current_balance = total_income - total_expenses
        
        # Build financial summary
        summary = f"""
FINANCIAL DATA SUMMARY:
- Total Income: ₱{total_income:,.2f}
- Total Expenses: ₱{total_expenses:,.2f}
- Current Balance: ₱{current_balance:,.2f}
- Total Saved: ₱{total_saved:,.2f}

INCOME BREAKDOWN:
"""
        for income in incomes:
            summary += f"  • {income.get_category()}: ₱{income.get_amount():,.2f} - {income.get_desc()}\n"
        
        summary += "\nEXPENSE BREAKDOWN:\n"
        for expense in expenses:
            summary += f"  • {expense.get_category()}: ₱{expense.get_amount():,.2f} - {expense.get_desc()}\n"
        
        summary += "\nSAVINGS GOALS:\n"
        for savings_goal in savings:
            progress = savings_goal.get_progress()
            summary += f"  • {savings_goal.get_name()}: ₱{savings_goal.get_saved():,.2f}/₱{savings_goal.get_cost():,.2f} ({progress:.1f}% complete)\n"
        
        return summary
    
    def chat(self, user_message, logic):
        """Send a message and get AI response from Groq"""
        # Get updated financial summary
        financial_summary = self.get_financial_summary(logic)
        
        # Build the system prompt
        system_prompt = f"""You are the AI Financial Coach for "Trakki", a personal finance tracking app. Your goal is to guide, motivate, and advise the user on their financial journey.

Here is the user's current financial data:
{financial_summary}

ROLE & TONE:
- Act like a supportive, financially-savvy Filipino friend or mentor. Be approachable, empathetic, and strictly non-judgmental.
- Use natural, modern english.

YOUR TASK:
- Analyze their specific financial data to provide highly personalized, actionable advice.
- If they are hitting savings goals or keeping expenses low, give them positive reinforcement.
- If their expenses are dangerously close to (or exceeding) their income, offer a gentle, practical warning and a quick tip to adjust.

STRICT CONSTRAINTS:
1. LANGUAGE: You MUST respond ONLY in English. 
2. LENGTH: Keep responses concise and easy to read (1-2 paragraphs), unless the user explicitly asks for a longer explanation.
3. SCOPE: Never invent data. Base your advice strictly on the provided financial summary.
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
