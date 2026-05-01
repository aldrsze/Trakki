from logic.models import Expense, Income, Target, SavingsTransaction

class TrakkiLogic:
    SAMPLE_INCOMES = [
        (4500.00, "Primary Salary", "Monthly base pay from employer", "2026-04-01 09:00:00"),
        (850.00, "Side Hustle", "E-commerce store monthly profit", "2026-04-10 14:30:00"),
        (1000.00, "Real Estate", "Rental property income", "2026-04-15 10:00:00"),
        (120.00, "Investments", "Quarterly dividend payouts", "2026-04-20 11:15:00"),
    ]

    SAMPLE_EXPENSES = [
        (1500.00, "Housing", "Monthly rent/mortgage payment", "2026-04-02 08:00:00"),
        (400.00, "Groceries", "Weekly supermarket runs", "2026-04-05 18:45:00"),
        (200.00, "Utilities", "Electricity, Water, and Fiber Internet", "2026-04-08 09:30:00"),
        (350.00, "Transportation", "Car loan and gas", "2026-04-12 17:20:00"),
        (150.00, "Dining Out", "Weekend restaurants and cafes", "2026-04-16 20:00:00"),
        (50.00, "Health", "Monthly Gym Membership", "2026-04-18 07:00:00"),
        (45.00, "Subscriptions", "Netflix, Spotify, and Cloud Storage", "2026-04-21 10:00:00"),
        (120.00, "Personal", "Clothing and personal care", "2026-04-25 15:30:00"),
    ]

    SAMPLE_TARGETS = [
        ("Japan Trip 2027", 4000.00, "2027-11-10 00:00:00", 500.00, "2026-04-03 12:00:00"),
        ("House Down Payment", 30000.00, "2030-01-01 00:00:00", 1000.00, "2026-04-07 10:00:00"),
        ("New Smartphone", 1000.00, "2026-08-15 00:00:00", 450.00, "2026-04-14 16:00:00"),
        ("6-Month Emergency Fund", 12000.00, "2026-12-31 00:00:00", 800.00, "2026-04-19 09:00:00"),
        ("Christmas Gifts", 500.00, "2026-12-01 00:00:00", 100.00, "2026-04-26 14:00:00"),
    ]

    def __init__(self):
        # Encapsulation
        self.__expenses = []
        self.__incomes = []
        self.__savings = []
        self.__savings_transactions = []
        self.__next_income_id = 1
        self.__next_expense_id = 1
        self.__next_target_id = 1
        self.__next_savings_transaction_id = 1

        self._load_sample_data()

    # Instance Methods to retrieve the encapsulated lists
    def get_expenses(self): 
        return self.__expenses
    
    def get_incomes(self): 
        return self.__incomes
    
    def get_savings(self): 
        return self.__savings

    def get_savings_transactions(self):
        return self.__savings_transactions

    def _load_sample_data(self):
        for amount, category, desc, date_string in self.SAMPLE_INCOMES:
            self.add_income(amount, category, desc, date_string)

        for amount, category, desc, date_string in self.SAMPLE_EXPENSES:
            self.add_expense(amount, category, desc, date_string)

        for name, cost, goal_date, saved_amount, created_at in self.SAMPLE_TARGETS:
            self.add_target(name, cost, goal_date, saved_amount, created_at)

        self._seed_savings_transactions()

    def _seed_savings_transactions(self):
        for target in self.__savings:
            if target.get_saved() > 0:
                self.add_savings_transaction(
                    target.get_target_id(),
                    target.get_name(),
                    target.get_saved(),
                    target.get_created_at()
                )

    # Instance Methods to ADD new data using the Models
    def add_expense(self, amount, category, desc, date_string=None):
        new_expense = Expense(self.__next_expense_id, amount, category, desc, date_string)
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

    def add_income(self, amount, category, desc, date_string=None):
        new_income = Income(self.__next_income_id, amount, category, desc, date_string)
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

    def add_target(self, name, cost, date, saved=0.0, created_at=None):
        new_target = Target(self.__next_target_id, name, cost, date, saved, created_at)
        self.__savings.append(new_target)
        self.__next_target_id += 1 # increase per add

    def add_savings_transaction(self, target_id, target_name, amount, date_string=None):
        new_transaction = SavingsTransaction(
            self.__next_savings_transaction_id,
            target_id,
            target_name,
            amount,
            date_string
        )
        self.__savings_transactions.append(new_transaction)
        self.__next_savings_transaction_id += 1

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
