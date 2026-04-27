from logic.models import Expense, Income, Target

class TrakkiLogic:
    def __init__(self):
        # Encapsulation
        self.__expenses = [
            Expense("₱3,000.00", "Salary", "Main monthly salary.")
        ]
        self.__incomes = [
            Income("₱150.00", "Freelance", "Completed design project.")
        ]
        self.__targets = [
             Target("New Laptop", "₱1,200.00", "Dec 25, 2026", saved="₱850.00", progress=70.8)
        ]

    # Instance Methods to retrieve the encapsulated lists
    def get_expenses(self): 
        return self.__expenses
    
    def get_incomes(self): 
        return self.__incomes
    
    def get_targets(self): 
        return self.__targets

    # Instance Methods to ADD new data using the Models
    def add_expense(self, amount, category, desc):
        # Create a new Expense Object
        new_expense = Expense(f"₱{amount}", category, desc)
        self.__expenses.append(new_expense) 

    def add_income(self, amount, category, desc):
        new_income = Income(f"₱{amount}", category, desc)
        self.__incomes.append(new_income)

    def add_target(self, name, cost, date):
        new_target = Target(name, f"₱{cost}", date)
        self.__targets.append(new_target)