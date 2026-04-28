from logic.models import Expense, Income, Target

class TrakkiLogic:
    def __init__(self):
        # Encapsulation
        self.__expenses = []
        self.__incomes = []
        self.__targets = [
             Target("New Laptop", 1200.00, "Dec 25, 2026", 750.00)
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
        new_expense = Expense(amount, category, desc)
        self.__expenses.append(new_expense) 

    def add_income(self, amount, category, desc):
        new_income = Income(amount, category, desc)
        self.__incomes.append(new_income)

    def add_target(self, name, cost, date):
        new_target = Target(name, cost, date)
        self.__targets.append(new_target)

    def total_income(self):
        total = 0
        for income in self.get_incomes():
            amount = income.get_amount()
            total += float(str(amount))

        return total

    def total_expenses(self):
        total = 0
        for expense in self.get_expenses():
            amount = expense.get_amount()
            total += float(str(amount))

        return total
    
    def total_savings(self):
        total = 0
        for target in self.get_targets():
            amount = target.get_saved()
            total += float(str(amount))
        
        return total
