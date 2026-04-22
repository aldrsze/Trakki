import time
import msvcrt
import getpass
from datetime import datetime

class Expense:
    def __init__(self, expense_id, amount, category, description):
        self.expense_id = expense_id
        self.amount = amount
        self.category = category
        self.description = description
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Trakki:
    # Clears the screen
    CLS = "\033[H\033[2J"

    current_user = None
    balance = 0
    income = 0
    monthly_expenses = 0
    savings_rate = .0
    total_targets = 0

    def clear(self):
        print(self.CLS, end="")

    def __init__(self):
        self.expenses = []
        self.incomes = []
        self.users = []
    
    def login_panel(self):
        self.clear()
        w = 62
        print("="*w)
        print(" - LOGIN ACCOUNT - ".center(w))
        print("="*w)
        print()
        print("\033[4;1H USERNAME: ".center(w))
        print("\033[5;1H PASSWORD: ".center(w))
        print("="*w)
        print("[1] START TYPING [2] RETURN [3] SIGNUP".center(w))
        print("="*w)

        choice = input(" > ")

        if choice == '1':
            print("\033[7;1H\033[K", end="")
            print("INPUT DETAILS".center(w))

            username = input("\033[4;12H")
            password = getpass.getpass("\033[5;12H", echo_char='*')

            print("\033[7;1H\033[K", end="")
            print("[ENTER] TO SUBMIT [R] TO RESET".center(w))

            while True:
                choice1 = input("\n >  ").lower() 
                if choice1 == '':
                    auth_user = None
                    for user in self.users:
                        if username == user.username and password == user.password:
                            auth_user = username
                            self.current_user = username
                            break

                    if auth_user:
                        print("\033[7;1H\033[K", end="")
                        print("LOGIN SUCCESSFUL!".center(w))
                        input("\n >  [ENTER] TO CONTINUE")
                        self.dashboard_panel()
                        return
                    else:
                        print("\033[7;1H\033[K", end="")
                        print("INVALID USERNAME OR PASSWORD.".center(w))
                        input("\n >  [ENTER] TO CONTINUE")
                        break
                        
                elif choice1 == 'r':
                    break
                else:
                    pass
            self.login_panel()
        elif choice == '2':
            return
        elif choice == '3':
            self.signup_panel()
        else:
            self.login_panel()

    def signup_panel(self):
        w = 62
        print()
        print("="*w)
        print(" - CREATE ACCOUNT - ".center(w))
        print("="*w)
        print()
        print("\033[14;1H CREATE USERNAME: ".center(w))
        print("\033[15;1H CREATE PASSWORD: ".center(w))
        print("="*w)
        print("[1] START TYPING [2] RETURN".center(w))
        print("="*w)

        choice = input(" > ")

        if choice == '1':
            print("\033[17;1H\033[K", end="")
            print("INPUT DETAILS".center(w))
            
            username = input("\033[14;19H")
            password = getpass.getpass("\033[15;19H", echo_char='*')

            print("\033[17;1H\033[K", end="")
            print("[ENTER] TO SAVE [R] TO RESET".center(w))

            while True:
                choice1 = input("\n >  ").lower()
                
                if choice1 == '':
                    user_exist = False
                    for user in self.users:
                        if username == user.username:
                            user_exist = True
                            break
                    if user_exist:
                        print("\033[17;1H\033[K", end="")
                        print("USERNAME ALREADY EXIST".center(w))
                        input("\n >  [ENTER] TO CONTINUE")
                        self.signup_panel()
                        return
                    else:
                        new_user = User(username, password)
                        self.users.append(new_user)
                        print("\033[17;1H\033[K", end="")
                        print("ACCOUNT CREATED SUCCESSFULLY! ".center(w))
                        input("\n >  [ENTER] TO CONTINUE")
                        return

                elif choice1 == 'r':
                    self.signup_panel()
                    return
                else:
                    pass
        elif choice == '2':
            self.login_panel()
        else:
            self.signup_panel()
        
    def about_panel(self):
        self.clear()
        w = 62

        print("="*(w - 2))
        print("ABOUT TRAKKI".center(w - 2))
        print("".center(w - 2, "="))
        print("".center(w - 2))
        print(" TRAKKI is a specialized CLI financial tool designed to".ljust(w-2))
        print(" empower students to take control of their spending.".ljust(w-2))
        print("".center(w - 2))
        print(" CORE CAPABILITIES:".ljust(w-2))
        print(" - Track dynamic income (Scholarships, Allowances, Jobs)".ljust(w-2))
        print(" - Monitor student-centric expense categories".ljust(w-2))
        print(" - AI-powered Chat Advisor for personalized budgeting".ljust(w-2))
        print("".center(w - 2))
        print(" DEVELOPER: Aldrsze.".ljust(w-2))
        print("".center(w - 2))
        print("".center(w - 2, "="))
        print("[B] BACK TO HOME".center(w - 2))
        print("="*(w - 2))
        
        while True:
            choice = input(" > ").lower()

            if choice == 'b':
                return
            else:
                pass

    def dashboard_panel(self):
        self.clear()
        w = 62

        print("="*(w - 2))
        print(f"TRAKKI DASHBOARD | Welcome, [{self.current_user}]".center(w - 2))
        print("".center(w - 2, "="))
        print("".center(w - 2))
        print(f"   CURRENT BALANCE: ₱ {self.balance}".ljust(w-2))
        print("".center(w - 2))
        print(f"   || INCOME (MONTHLY): {self.income}".ljust(w-2))
        print(f"   || EXPENSES (MONTHLY): {self.monthly_expenses}".ljust(w-2))
        print(f"   || SAVINGS RATE : {self.savings_rate}".ljust(w-2))
        print(f"   || TOTAL TARGETS : {self.total_targets}".ljust(w-2))
        print("".center(w - 2))
        print("".center(w - 2, "═"))
        print(" [1] INCOME    [2] EXPENSES  [3] TARGETS".center(w - 2))
        print(" [4] HISTORY   [5] CHAT      [0] LOGOUT".center(w - 2))
        print("="*(w - 2))

        while True:
            choice = input(" > ")

            if choice == '1':
                self.income_panel()
            elif choice == '2':
                self.expenses_panel()
            elif choice == '3':
                self.targets_panel()
            elif choice == '4':
                self.table_panel()
            elif choice == '5':
                self.chat_panel()
            elif choice == '0':
                return
            else:
                pass
    
    def income_panel(self):
        self.clear()
        print("=")


    def expenses_panel(self):
        self.clear()
        print("expense_panel")
        input()
    def targets_panel(self):
        self.clear()
        print("targets panel")
        input()
    def table_panel(self):
        self.clear()
        print("table panel")
        input()
    def chat_panel(self):
        self.clear()
        print("chat panel")
        input()



    def home_panel(self):

        w = 62
        
        while True:
            self.clear()
            print("="*w)
            text = """
     ╔╦╦╦╦╦╦╗  ╔╦╦╦╦╗   ╔╦╦╦╦╦   ╔╗ ╔═    ╔╗ ╔═  ╔╦╦╦╦╗
        ║║     ║║  ║║   ║║  ║║   ║║ ║     ║║ ║     ║║
        ║║     ╠╬╬╬╬╩   ╠╬╬╬╬╣   ╠╬╬╬     ╠╬╬╬     ║║
        ║║     ║║  ╚╗   ║║  ║║   ║║ ╚╗    ║║ ╚╗    ║║
        ╩╩     ╩╩   ╩╩  ╩╩  ╩╩   ╩╩  ╩╩   ╩╩  ╩╩ ╚╩╩╩╩╝
                    """
            print(text.center(w))
            print("- YOUR PERSONAL EXPENSE TRACKER -\n".center(w))
            print("="*w)
            print()
            print("[1] LOGIN  [2] ABOUT  [0] EXIT\n".center(w))
            print("="*w)

            choice = input(" > ")

            if choice == '1':
                self.login_panel()
            elif choice == '2':
                self.about_panel()
            elif choice == '0':
                frames = [".  ", ".. ", "...", "   "]

                for i in range(15):
                    msg = f" Exiting {frames[i % 4]}"
                    print(msg.center(w), end="\r")
                    time.sleep(0.1)
                print("\033[K", end="") # Clear the line
                print("- Thank you for using the system -".center(w))
                time.sleep(0.5)
                return False
            else:
                pass

if __name__ == "__main__":
    Trakki = Trakki()
    user = User('admin', 'asd')
    Trakki.users.append(user)
    Trakki.clear()
    Trakki.home_panel()


