from datetime import datetime

class Expense:
    def __init__(self, amount, category, desc):
        # Encapsulation
        self.__amount = amount
        self.__category = category
        self.__desc = desc
        self.__date = datetime.now().strftime("%B %d, %Y")

    # Instance Methods (Getters) to safely read private data
    def get_amount(self): return self.__amount
    def get_category(self): return self.__category
    def get_desc(self): return self.__desc
    def get_date(self): return self.__date

class Income:
    def __init__(self, amount, category, desc):
        self.__amount = amount
        self.__category = category
        self.__desc = desc
        self.__date = datetime.now().strftime("%B %d, %Y")

    def get_amount(self): 
        return self.__amount

    def get_category(self):
        return self.__category

    def get_desc(self):
        return self.__desc

    def get_date(self):
        return self.__date

class Target:
    def __init__(self, name, cost, date, saved="₱0.00", progress=0):
        self.__name = name
        self.__cost = cost
        self.__saved = saved
        self.__needed = cost
        self.__progress = progress
        self.__date = date

    def get_name(self): 
        return self.__name

    def get_cost(self):
        return self.__cost

    def get_saved(self):
        return self.__saved

    def get_needed(self):
        return self.__needed

    def get_progress(self):
        return self.__progress

    def get_date(self):
        return self.__date