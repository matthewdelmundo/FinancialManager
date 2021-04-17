from calendar import isleap
from datetime import date
import kivy
from kivy.storage.jsonstore import JsonStore


# Main class that holds the functions for reading and writing data
class Database:
    def __init__(self):
        self.index = 0
        self.data = JsonStore("data.json", indent=2, sort_keys=True)
        self.current_date = self.get_current_date_data()
        self.test_json()

    def test_json(self):
        self.data.put("2021-4-10", entries=["Hey", "Ho"])
        self.data.put("2021-4-15", entries=["hi"])
        self.data.put("2022-1-1", entries=["hello"])

    def update_current_date(self, current_date):
        self.current_date = current_date

    def get_current_date_data(self):
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

    def Test(self):
        print(self.current_date)
