from datetime import date
import kivy
from kivy.storage.jsonstore import JsonStore

from database import get_date_id


class BudgetDatabase:
    def __init__(self, database):
        self.database = database
        self.date_today = self.database.date_today

        self.budgets = JsonStore("data/budgets.json", indent=2, sort_keys=True)

    def load_budgets(self):
        budgets = []
        for budget_ind in self.budgets:
            budget = self.budgets.get(budget_ind)
            budget_tuple = (budget["Name"], budget["Total"], budget["Source"])
            budgets.append(budget_tuple)
        return budgets

    def save_budget(self, index, name, total, source):
        self.budgets.put(index, Name=name, Total=total, Source=source)

    def get_current_date(self):
        return self.date_today

    def get_budget_expense(self, budget_name):
        date_id = get_date_id(self.date_today)
        return self.database.get_budget_expense(date_id, budget_name)