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


# Main class that holds the functions for reading and writing data
class Database:
    def __init__(self):
        self.index = 0
        self.data = JsonStore("data/data.json", indent=2, sort_keys=True)
        # cached date upon opening the app
        self.date_today = self.get_date_today()
        # current_date will change depending on which date is chosen in the calendar
        self.current_date = self.get_date_today()
        self.test_json()

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

    def save_entries_list(self, entries_list):
        date_id = get_date_id(self.current_date)
        self.data.put(date_id, entries=entries_list)

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

    def delete_entries_list(self):
        date_id = get_date_id(self.current_date)
        if self.data.exists(date_id):
            self.data.delete(date_id)

    def update_current_date(self, current_date):
        self.current_date = current_date

    def get_current_date(self):
        return self.current_date

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
