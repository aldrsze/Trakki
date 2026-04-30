from logic.models import Expense, Income, Target

class TrakkiLogic:
    def __init__(self):
        # Encapsulation
        self.__expenses = []
        self.__incomes = []
        self.__savings = []
        self.__next_income_id = 1
        self.__next_expense_id = 1
        self.__next_target_id = 1
        
        # Sample Income Data
        self.add_income(4500.00, "Primary Salary", "Monthly base pay from employer")
        self.add_income(850.00, "Side Hustle", "E-commerce store monthly profit")
        self.add_income(1000.00, "Real Estate", "Rental property income")
        self.add_income(120.00, "Investments", "Quarterly dividend payouts")

        # Sample Expense Data
        self.add_expense(1500.00, "Housing", "Monthly rent/mortgage payment")
        self.add_expense(400.00, "Groceries", "Weekly supermarket runs")
        self.add_expense(200.00, "Utilities", "Electricity, Water, and Fiber Internet")
        self.add_expense(350.00, "Transportation", "Car loan and gas")
        self.add_expense(150.00, "Dining Out", "Weekend restaurants and cafes")
        self.add_expense(50.00, "Health", "Monthly Gym Membership")
        self.add_expense(45.00, "Subscriptions", "Netflix, Spotify, and Cloud Storage")
        self.add_expense(120.00, "Personal", "Clothing and personal care")

        # Sample Target Data (Savings Goals)
        self.add_target("Japan Trip 2027", 4000.00, "Nov 10, 2027", 500.00)
        self.add_target("House Down Payment", 30000.00, "Jan 01, 2030", 1000.00)
        self.add_target("New Smartphone", 1000.00, "Aug 15, 2026", 450.00)
        self.add_target("6-Month Emergency Fund", 12000.00, "Dec 31, 2026", 800.00)
        self.add_target("Christmas Gifts", 500.00, "Dec 01, 2026", 100.00)

    # Instance Methods to retrieve the encapsulated lists
    def get_expenses(self): 
        return self.__expenses
    
    def get_incomes(self): 
        return self.__incomes
    
    def get_savings(self): 
        return self.__savings

    # Instance Methods to ADD new data using the Models
    def add_expense(self, amount, category, desc):
        new_expense = Expense(self.__next_expense_id, amount, category, desc)
        self.__expenses.append(new_expense) 
        self.__next_expense_id += 1 # increase per add
        
    def update_expense(self, expense_id, new_amount, new_category, new_desc):
        for expense in self.__expenses:
            if expense.get_expense_id() == expense_id:
                expense.set_amount(new_amount)
                expense.set_category(new_category)
                expense.set_desc(new_desc)
                break

    def remove_expense(self, expense_id):
        # remove expense by id
        for expense in range(len(self.__expenses)):
            if self.__expenses[expense].get_expense_id() == expense_id:
                self.__expenses.pop(expense)
                break  # Stop after finding and removing the first match

    def add_income(self, amount, category, desc):
        new_income = Income(self.__next_income_id, amount, category, desc)
        self.__incomes.append(new_income)
        self.__next_income_id += 1 # increase it per add

    def update_income(self, income_id, new_amount, new_category, new_desc):
        for income in self.__incomes:
            if income.get_income_id() == income_id:
                income.set_amount(new_amount)
                income.set_category(new_category)
                income.set_desc(new_desc)
                break
    
    def remove_income(self, income_id):
        # remove income by id 
        for income in range(len(self.__incomes)):
            if self.__incomes[income].get_income_id() == income_id:
                self.__incomes.pop(income)
                break  # Stop after finding and removing the first match

    def add_target(self, name, cost, date, saved=0.0):
        new_target = Target(self.__next_target_id, name, cost, date, saved)
        self.__savings.append(new_target)
        self.__next_target_id += 1 # increase per add

    def update_target(self, target_id, name, cost, date):
        for target in self.__savings:
            if target.get_target_id() == target_id:
                target.set_name(name)
                target.set_cost(cost)
                target.set_date(date)
                break

    def remove_target(self, target_id):
        # remove target by id
        for target in range(len(self.__savings)):
            if self.__savings[target].get_target_id() == target_id:
                self.__savings.pop(target)
                break  # Stop after finding and removing the first match

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
    
    def current_balance(self):
        income_total = self.total_income()
        expense_total = self.total_expenses()
        saved_total = self.total_saved()
        
        return income_total - expense_total - saved_total

    def total_saved(self):
        total = 0
        for target in self.get_savings():
            amount = target.get_saved()
            total += float(str(amount))
        return total
