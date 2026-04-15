from datetime import datetime

class Expense:
    def __init__(self, id, amount, category, description):
        self.id = id
        self.amount = float(amount)
        self.category = category
        self.description = description
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return f"{self.id}  | {self.date}  | ${self.amount:>8.2f} | {self.category:12} | {self.description}"

class Krakki:
    def __init__(self):
        self.expenses = []

    # Creating expense
    def add_expense(self):

        id = int(input("\nID : "))
        amount = float(input("Amount : "))
        category = input("Category : ")
        description = input("Description : ")

        if amount <= 0:
            print("Invalid Amount.")
            return
        
        new_expense = Expense(id, amount, category, description)
        self.expenses.append(new_expense)

        print("Expense Added Successfully!")

    def show_expenses(self):
        sum = 0

        print("\n" + "="*100)
        print(f"{'ID':2} | {'Date':20} | {'Amount':9} | {'Category':12} | {'Description'}")
        print("-" * 100)
        for e in self.expenses:
            sum += e.amount
            print(e)
        print("="*100)
        print(f"TOTAL SPENT: ${sum:.2f}")      
    
    def update_expense(self):
            
            id = int(input("\nID : "))
            new_amount = input("Updated Amount : ")
            new_category = input("Updated Category : ")
            new_description = input("Updated Description : ")

            for e in self.expenses:
                if e.id == id:
                    e.amount = float(new_amount) if new_amount else e.amount
                    e.category = new_category if new_category else e.category
                    e.description = new_description if new_description else e.description
                    print(f"Updated Expense ID: {id}")
    
    def delete_expense(self):
            
            id = int(input("Enter Expense ID to delete: "))

            for e in self.expenses:
                if e.id == id:
                    self.expenses.remove(e)
                    print(f"Expense ID: {id} removed successfully.")
            
    def menu(self):
        while True:
            print(f"\n1. View All Expenses")
            print(f"2. Add Expenses")
            print(f"3. Update Expenses")
            print(f"4. Delete Expenses")
            print(f"5. Exit")

            try:
                choice = input("Select Option (1-5): ")
                if choice == '1': self.show_expenses()
                elif choice == '2': self.add_expense()
                elif choice == '3': self.update_expense()
                elif choice == '4': self.delete_expense()
                elif choice == '5': break
                else:
                    print("invalid choice.")
            except Exception as e:
                print(f"error: ", e)

             
Krakki = Krakki()

Krakki.menu()










