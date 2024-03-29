from calendar import isleap
from datetime import date
import kivy
from kivy.storage.jsonstore import JsonStore

month_converter = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

def convert_month_num(month_num):
    return month_converter[month_num]


def get_date_id(chosen_date):
    return "-".join([str(chosen_date[2]), str(chosen_date[1]), str(chosen_date[0])])


def create_entry_dict(name, type, category, amount):
    return {"Name": name,
            "Type": type,
            "Category": category,
            "Amount": amount}


# Main class that holds the functions for reading and writing entries
class Database:
    def __init__(self):
        self.index = 0
        
        self.data = JsonStore("data/data.json", indent=2, sort_keys=True)

        # cached date upon opening the app
        self.date_today = self.get_date_today()

        # current_date will change depending on which date is chosen in the calendar
        self.current_date = self.get_date_today()

        self.categorize_json_content()

    # Initializing test database content
    def test_json(self):
        self.data.put("2021-4-10", entries=[{"Name": "Ice Cream",
                                             "Type": "Expense",
                                             "Category": "Snacks",
                                             "Amount": 350.0}])
        self.data.put("2021-4-15", entries=[{"Name": "Grocery Run",
                                             "Type": "Expense",
                                             "Category": "Groceries",
                                             "Amount": 469.99},
                                            {"Name": "Grab Fare",
                                             "Type": "Expense",
                                             "Category": "Transportation",
                                             "Amount": 120.0}])
        self.data.put("2022-1-1", entries=[{"Name": "Salary",
                                            "Type": "Income",
                                            "Category": None,
                                            "Amount": 50000.0}])
    
    # Deletes an income/expense entry from database
    def delete_ent_from_db(self, index):
        date_id = get_date_id(self.current_date)
        entry_list = self.data.get(date_id)["entries"]
        entry_list.pop(index)

        # Update category list too!
        new_exp_cat_list = self.get_categories_dict(entry_list)

        if len(entry_list) == 0 and self.data.exists(date_id):
            self.data.delete(date_id)
        else:
            self.data.put(date_id, entries=entry_list, 
                expense_categories=new_exp_cat_list)   

    # Deletes list of entries under current date                
    def delete_entries_list(self):
        date_id = get_date_id(self.current_date)
        if self.data.exists(date_id):
            self.data.delete(date_id)

    # Adds Income & Budget Category lists to the default/hardcoded data
    def categorize_json_content(self):
        for date_id in self.data:
            entry_dict_list = self.data.get(date_id)["entries"]
            expense_category_dict = self.get_categories_dict(entry_dict_list)

            self.data.put(date_id, entries=entry_dict_list,
                          expense_categories=expense_category_dict)

    # Puts data to the database based on the newly added/updated entries list and expense
    # category list
    def save_entries_list(self, entries_list):
        date_id = get_date_id(self.current_date)
        expense_category_dict = self.get_categories_dict(entries_list)

        self.data.put(date_id, entries=entries_list,
                      expense_categories=expense_category_dict)

    # Saving categories list  
    def get_categories_dict(self, entries_list):
        expense_category_dict = {}
        
        for i in range(len(entries_list)):
            entry_dict = entries_list[i]
            entry_type = entry_dict["Type"]
            entry_category = entry_dict["Category"]
            entry_amount = entry_dict["Amount"]

            if entry_type == "Income":
                continue

            if entry_category in expense_category_dict:
                expense_category_dict[entry_category] += entry_amount
            else:
                expense_category_dict[entry_category] = entry_amount

        return expense_category_dict

    def get_budget_expense(self, date_id, budget_name):
        expense = 0
        if self.data.exists(date_id):
            expense_categories = self.data.get(date_id)["expense_categories"]
            if budget_name in expense_categories:
                expense = expense_categories[budget_name]
        return expense

    def get_expense_categories_list(self, view_date):
        date_id = get_date_id(view_date)
        expense_categories_list = []

        if self.data.exists(date_id):
            expense_categories_dict = self.data.get(date_id)["expense_categories"]

            for expense_name in expense_categories_dict:
                expense_categories_list.append((expense_name,
                                                expense_categories_dict[expense_name]))

        return expense_categories_list

    def get_total_income(self, view_date):
        date_id = get_date_id(view_date)
        total_income = 0

        if self.data.exists(date_id):
            entry_dict_list = self.data.get(date_id)["entries"]

            for entry_dict in entry_dict_list:
                entry_type = entry_dict["Type"]
                entry_amount = entry_dict["Amount"]

                if entry_type == "Income":
                    total_income += entry_amount

        return total_income

    def get_total_expense(self, view_date):
        expense_categories_list = self.get_expense_categories_list(view_date)
        total_expense = 0

        for expense in expense_categories_list:
            total_expense += expense[1]

        return total_expense

    def load_entries_list(self):
        date_id = get_date_id(self.current_date)
        entries_list = []

        if self.data.exists(date_id):
            entry_dict_list = self.data.get(date_id)["entries"]
            for i in range(len(entry_dict_list)):
                entry_dict = entry_dict_list[i]
                entry = [entry_dict["Name"], entry_dict["Type"],
                         entry_dict["Category"], entry_dict["Amount"]]
                entries_list.append(entry)

        return entries_list

    def update_current_date(self, current_date):
        self.current_date = current_date

    def get_current_date(self):
        return [self.current_date[0], self.current_date[1], self.current_date[2]]

    def get_date_today(self):
        current_date = date.today()
        current_year = current_date.year
        current_month = current_date.month
        current_day = current_date.day

        return [current_day, current_month, current_year]

    def is_date_in_database(self, chosen_date):
        date_key = str(chosen_date[2]) + "-" + str(chosen_date[1]) + \
                   "-" + str(chosen_date[0])
        if self.data.exists(date_key):
            return True
        return False

    def print_value(self):
        print(self.data.get("2021-4-10")["entries"][0])
        print(get_date_id(self.current_date))

    #calculates the total sum of entries
    #Note that expense entries are entered in database as positive values
    def get_all_entries_total(self):
        total = 0
        datalist = self.data.keys()
        for i in range(len(datalist)):
            entries_list = self.data.get(datalist[i])["entries"]
            for j in range(len(entries_list)):
                amount = entries_list[j]["Amount"]
                if entries_list[j]["Type"] == "Income":
                    total += amount
                elif entries_list[j]["Type"] == "Expense":
                    total -= amount
        return total
