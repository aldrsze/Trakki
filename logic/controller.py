from logic.models import Expense, Income, Target

class TrakkiLogic:
    def __init__(self):
        # Encapsulation
        self.__expenses = []
        self.__incomes = []
        self.__targets = []
        self.__next_income_id = 1
        self.__next_expense_id = 1
        self.__next_target_id = 1

        # Sample Income Data
        self.add_income(5000, "Salary", "Monthly salary from work")
        self.add_income(500, "Freelance", "Web design project")
        self.add_income(200, "Investment", "Dividend payout")

        # Sample Expense Data
        self.add_expense(1200, "Rent", "Monthly apartment rent")
        self.add_expense(300, "Groceries", "Weekly grocery shopping")
        self.add_expense(150, "Utilities", "Electricity and water bills")
        self.add_expense(100, "Transportation", "Gas and public transport")
        self.add_expense(80, "Entertainment", "Movie and dinner")
        self.add_expense(200, "Healthcare", "Medicine and clinic visit")

        # Sample Target Data (Savings Goals)
        self.add_target("New Laptop", 1200.00, "Dec 25, 2026", 750.00)
        self.add_target("Vacation", 3000.00, "Jun 15, 2026", 1500.00)
        self.add_target("Emergency Fund", 5000.00, "Dec 31, 2026", 2000.00)
        self.add_target("Car Down Payment", 10000.00, "Mar 20, 2027", 4500.00)

    # Instance Methods to retrieve the encapsulated lists
    def get_expenses(self): 
        return self.__expenses
    
    def get_incomes(self): 
        return self.__incomes
    
    def get_targets(self): 
        return self.__targets

    # Instance Methods to ADD new data using the Models
    def add_expense(self, amount, category, desc):
        new_expense = Expense(self.__next_expense_id, amount, category, desc)
        self.__expenses.append(new_expense) 
        self.__next_expense_id += 1 # increase per add

    def add_income(self, amount, category, desc):
        new_income = Income(self.__next_income_id, amount, category, desc)
        self.__incomes.append(new_income)
        self.__next_income_id += 1 # increase it per add

    def add_target(self, name, cost, date, saved=0.00):
        new_target = Target(self.__next_target_id, name, cost, date, saved)
        self.__targets.append(new_target)
        self.__next_target_id += 1 # increase per add

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
    
    def remove_income(self, income_id):
        # remove income by id 
        for income in range(len(self.__incomes)):
            if self.__incomes[income].get_income_id() == income_id:
                self.__incomes.pop(income)
                break  # Stop after finding and removing the first match

    def remove_expense(self, expense_id):
        # remove expense by id
        for expense in range(len(self.__expenses)):
            if self.__expenses[expense].get_expense_id() == expense_id:
                self.__expenses.pop(expense)
                break  # Stop after finding and removing the first match

    def remove_target(self, target_id):
        # remove target by id
        for target in range(len(self.__targets)):
            if self.__targets[target].get_target_id() == target_id:
                self.__targets.pop(target)
                break  # Stop after finding and removing the first match