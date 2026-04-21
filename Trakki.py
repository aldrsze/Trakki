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
    HORZ      = "═"
    VERT      = "║"
    TOP_LEFT  = "╔"
    TOP_RIGHT = "╗"
    BOT_LEFT  = "╚"
    BOT_RIGHT = "╝"
    T_RIGHT   = "╠"  
    T_LEFT    = "╣"
    T_DOWN    = "╦"
    T_UP      = "╩"
    CROSS     = "╬"

    def clear(self):
        print(self.CLS, end="")
    
    def clear_buffer(self):
        while msvcrt.kbhit():
            msvcrt.getch()

    def __init__(self):
        self.expenses = []
        self.users = []
    
    def login_panel(self):
        self.clear()
        w = 62
        print("═"*w)
        print(" - LOGIN ACCOUNT - ".center(w))
        print("═"*w)
        print()
        print("\033[4;1H USERNAME: ".center(w))
        print("\033[5;1H PASSWORD: ".center(w))
        print("═"*w)
        print("[1] START TYPING [2] RETURN".center(w))
        print("═"*w)

        choice = msvcrt.getch().decode('utf-8').lower()

        if choice == '1':
            print("\033[7;1H\033[K", end="")
            print("INPUT DETAILS".center(w))

            username = input("\033[4;12H")
            password = getpass.getpass("\033[5;12H", echo_char='*')

            print("\033[7;1H\033[K", end="")
            print("[ENTER] TO SUBMIT [R] TO RESET".center(w))

            while True:
                choice1 = msvcrt.getch().decode('utf-8').lower()
                if choice1 == '\r':
                    current_user = None
                    for user in self.users:
                        if username == user.username and password == user.password:
                            current_user = username
                            break

                    if current_user:
                        print("\033[7;1H\033[K", end="")
                        print("LOGIN SUCCESSFUL!".center(w))
                        self.dashboard_panel()
                        return
                    else:
                        print("\033[7;1H\033[K", end="")
                        print("INVALID USERNAME OR PASSWORD.".center(w))
                        self.clear_buffer()
                        break
                        
                elif choice1 == 'r':
                    break
                else:
                    pass
            self.login_panel()
        elif choice == '2':
            return
        else:
            self.clear_buffer()
            self.login_panel()

    def signup_panel(self):
        self.clear()
        w = 62
        print("═"*w)
        print(" - CREATE ACCOUNT - ".center(w))
        print("═"*w)
        print()
        print("\033[4;1H CREATE USERNAME: ".center(w))
        print("\033[5;1H CREATE PASSWORD: ".center(w))
        print("═"*w)
        print("[1] START TYPING [2] RETURN".center(w))
        print("═"*w)

        choice = msvcrt.getch().decode('utf-8').lower()

        if choice == '1':
            print("\033[7;1H\033[K", end="")
            print("INPUT DETAILS".center(w))
            
            username = input("\033[4;19H")
            password = getpass.getpass("\033[5;19H", echo_char='*')

            print("\033[7;1H\033[K", end="")
            print("[ENTER] TO SAVE [R] TO RESET".center(w))

            while True:
                choice1 = msvcrt.getch().decode('utf-8').lower()
                
                if choice1 == '\r': # \r is enter key
                    user_exist = False
                    for user in self.users:
                        if username == user.username:
                            user_exist = True
                            break
                    if user_exist:
                        print("\033[7;1H\033[K", end="")
                        print("USERNAME ALREADY EXIST".center(w))
                        msvcrt.getch()
                        time.sleep(0.1)
                        self.signup_panel()
                        return
                    else:
                        new_user = User(username, password)
                        self.users.append(new_user)
                        print("\033[7;1H\033[K", end="")
                        print("ACCOUNT CREATED SUCCESSFULLY! ".center(w))
                        msvcrt.getch()
                        return

                elif choice1 == 'r':
                    self.signup_panel()
                    return
                else:
                    pass
        elif choice == '2':
            return
        else:
            self.clear_buffer()
            self.signup_panel()
        
    def about_panel(self):
        self.clear()
        input()
    def dashboard_panel(self):
        self.clear()
        print("dashboard")
        input()
    def income_panel(self):
        self.clear()
        print("income panel")
        input()
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
            print("═"*w)
            text = """
      ╔╦╦╦╦╦╗  ╔╦╦╦╦╗   ╔╦╦╦╦╦╗  ║║  ╔═╝  ║║  ╔═╝  ╔╦╦╦╗
        ║║     ║║  ║║   ║║  ║║   ║║ ║║    ║║ ║║      ║║
        ║║     ╠╬╬╬╩╗   ╠╬╬╬╬╣   ╠╬╬╩╗    ╠╬╬╩╗      ║║
        ║║     ║║ ╚╗    ║║  ║║   ║║ ╚╗    ║║ ╚╗      ║║
        ╩╩     ╩╩  ╩╩   ╩╩  ╩╩   ╩╩  ╩╩   ╩╩  ╩╩   ╩╩╩╩╩
                    """
            print(text.center(w))
            print("- YOUR PERSONAL EXPENSE TRACKER -\n".center(w))
            print("═"*w)
            print()
            print("[1] LOGIN   [2] SIGNUP".center(w))
            print("[3] ABOUT   [0] EXIT\n".center(w))
            print("═"*w)

            choice = msvcrt.getch().decode('utf-8').lower()

            if choice == '1':
                self.login_panel()
            elif choice == '2':
                self.signup_panel()
            elif choice == '3':
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
                self.clear_buffer()

if __name__ == "__main__":
    Trakki = Trakki()
    Trakki.clear()
    Trakki.home_panel()


