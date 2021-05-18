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

    def remove_budget(self, budget_name):
        keys = self.budgets.keys()
        for i in range(len(keys)):
            value = self.budgets.get(keys[i])
            if budget_name == value["Name"]:
                self.budgets.delete(keys[i])

    def reorganize_json(self):
        keys = self.budgets.keys()
        index = 0
        for i in range(len(keys)):
            key = keys[i]
            budget = self.budgets.get(key)
            budget_name = budget["Name"]
            budget_source = budget["Source"]
            budget_total = budget["Total"]

            self.budgets.delete(key)
            index = i + 1
            self.save_budget(str(index), budget_name, budget_total, budget_source)
        return index + 1