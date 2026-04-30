from datetime import datetime

class Expense:
    def __init__(self, expense_id, amount, category, desc, date_string=None):
        # Encapsulation
        self.__expense_id = expense_id
        self.__amount = amount
        self.__category = category
        self.__desc = desc

        # If a custom date is provided, use it. Otherwise, use right now.
        if date_string:
            self.__date = date_string
        else:
            self.__date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Instance Methods (Getters) to safely read private data
    def get_expense_id(self): return self.__expense_id
    def get_amount(self): return self.__amount
    def get_category(self): return self.__category
    def get_desc(self): return self.__desc
    def get_date(self): return self.__date

    def set_amount(self, amount):
        self.__amount = amount

    def set_category(self, category):
        self.__category = category

    def set_desc(self, desc):
        self.__desc = desc

class Income:
    def __init__(self, income_id, amount, category, desc, date_string=None):
        self.__income_id = income_id
        self.__amount = amount
        self.__category = category
        self.__desc = desc
        # If a custom date is provided, use it. Otherwise, use right now.
        if date_string:
            self.__date = date_string
        else:
            self.__date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_income_id(self): return self.__income_id
    def get_amount(self): return self.__amount
    def get_category(self): return self.__category
    def get_desc(self): return self.__desc
    def get_date(self): return self.__date

    def set_amount(self, amount):
        self.__amount = amount

    def set_category(self, category):
        self.__category = category

    def set_desc(self, desc):
        self.__desc = desc

class Target:
    def __init__(self, target_id, name, cost, date, saved=0.00, created_at=None):
        self.__target_id = target_id
        self.__name = name
        self.__cost = float(cost)
        self.__saved = float(saved)
        self.__date = date # goal date

        # creation date
        if created_at:
            self.__created_at = created_at
        else:
            self.__created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_target_id(self): return self.__target_id
    def get_name(self): return self.__name
    def get_cost(self): return self.__cost
    def get_saved(self): return self.__saved
    def get_needed(self):
        needed = float(self.__cost) - self.__saved
        return max(0, needed) # to not show negative
    def get_progress(self):
        if self.__cost == 0: return 0
        progress = (self.__saved / float(self.__cost)) * 100
        return max(0 ,min(100, progress)) # Caps at 100% and bottoms at 0%
    def get_date(self): return self.__date
    def get_created_at(self): return self.__created_at

    def set_name(self, name):
        self.__name = name

    def set_cost(self, cost):
        self.__cost = float(cost)

    def set_date(self, date):
        self.__date = date

    def set_saved(self, saved):
        self.__saved = float(saved)