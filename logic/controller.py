from logic.models import Expense, Income, Target, SavingsTransaction

class TrakkiLogic:
    SAMPLE_INCOMES = [
        (12000.00, "Monthly Allowance", "Living expense allowance from parents", "2026-04-01 09:00:00"),
        (3500.00, "Student Assistant Pay", "Salary for library/department assistant duties", "2026-04-10 14:30:00"),
        (2000.00, "Scholarship Stipend", "Monthly university/government scholarship award", "2026-04-15 10:00:00"),
        (1500.00, "Side Hustles", "Selling old clothes online & minor academic commissions", "2026-04-20 11:15:00"),
    ]
    # Total Monthly Income: 19,000.00

    SAMPLE_EXPENSES = [
        (4000.00, "Dorm Rent", "Shared boarding house / dorm room rent", "2026-04-05 18:45:00"),
        (5000.00, "Food & Groceries", "Campus meals, instant noodles, and convenience store runs", "2026-04-08 09:30:00"),
        (1000.00, "School Supplies", "Photocopying thick readings, index cards, and yellow pads", "2026-04-12 17:20:00"),
        (1200.00, "Transportation", "Daily commute & the occasional ride-hailing app when late", "2026-04-16 20:00:00"),
        (400.00, "Mobile Data", "Prepaid load promos for outdoor classes and group chats", "2026-04-18 07:00:00"),
        (600.00, "Caffeine & Snacks", "Iced coffee and energy drinks for finals week prep", "2026-04-21 10:00:00"),
        (250.00, "Subscriptions", "Spotify Premium Student & shared streaming account", "2026-04-25 15:30:00"),
        (250.00, "Org Expenses", "University organization shirt and event contributions", "2026-04-28 12:00:00"),
    ]
    # Total Monthly Expenses: 12,700.00
    # Remaining Cash Flow for Savings: 6,300.00

    SAMPLE_TARGETS = [
        ("Midterm Tuition Fund", 15000.00, "2026-05-15 00:00:00", 1000.00, "2026-04-02 08:00:00"),
        ("New Laptop Fund", 35000.00, "2026-09-01 00:00:00", 500.00, "2026-03-20 12:00:00"),
        ("Emergency Fund", 5000.00, "2026-12-31 00:00:00", 100.00, "2026-03-25 10:00:00"),
        ("Thesis & Defense Fees", 3000.00, "2026-06-15 00:00:00", 200.00, "2026-04-01 16:00:00")
    ]

    def __init__(self):
        # Encapsulation
        self.__expenses = []
        self.__incomes = []
        self.__savings = []
        self.__savings_transactions = []

        # for tracking the id of the models
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
        saved_total = self.total_savings()
        
        return income_total - expense_total - saved_total

    def total_savings(self):
        total = 0
        for target in self.get_savings():
            amount = target.get_saved()
            total += float(str(amount))
        return total
