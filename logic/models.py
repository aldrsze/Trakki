from datetime import datetime

class Expense:
    def __init__(self, expense_id, amount, category, desc):
        # Encapsulation
        self.__expense_id = expense_id
        self.__amount = amount
        self.__category = category
        self.__desc = desc
        self.__date = datetime.now().strftime("%B %d, %Y")

    # Instance Methods (Getters) to safely read private data
    def get_expense_id(self): return self.__expense_id
    def get_amount(self): return self.__amount
    def get_category(self): return self.__category
    def get_desc(self): return self.__desc
    def get_date(self): return self.__date

class Income:
    def __init__(self, income_id, amount, category, desc):
        self.__income_id = income_id
        self.__amount = amount
        self.__category = category
        self.__desc = desc
        self.__date = datetime.now().strftime("%B %d, %Y")

    def get_income_id(self): return self.__income_id
    def get_amount(self): return self.__amount
    def get_category(self): return self.__category
    def get_desc(self): return self.__desc
    def get_date(self): return self.__date

class Target:
    def __init__(self, target_id, name, cost, date, saved=0.00):
        self.__target_id = target_id
        self.__name = name
        self.__cost = float(cost)
        self.__saved = float(saved)
        self.__date = date

    def get_target_id(self): return self.__target_id
    def get_name(self): return self.__name
    def get_cost(self): return self.__cost
    def get_saved(self): return self.__saved
    def get_needed(self):
        needed = self.__cost - self.__saved
        return max(0, needed) # to not show negative
    def get_progress(self):
        if self.__cost == 0: return 0
        progress = (self.__saved / self.__cost) * 100
        return min(100, progress) # Caps at 100%
    def get_date(self): return self.__date