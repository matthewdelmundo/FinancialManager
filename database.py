from calendar import isleap
from datetime import date


# Holds lists of DailyData for each year
# Uses a DICT to identify years
class DataCalendar:
    def __init__(self):
        self.calendar_dict = self.generate_calendar()

    # Loads calender if existing data can be found
    # Creates new calender otherwise
    def generate_calendar(self):
        # TODO: Load calender if previous data is available
        # if (data_exists)
        #   return existing_data

        # Generates new calendar DICT with just the current year
        current_date = date.today()
        current_year = current_date.year
        return {current_year: self.Year(current_year)}

    # Returns DailyData given a date
    def get_data(self, year_num, month_num, day_num):
        return self.get_year(year_num).get_month(month_num).get_day(day_num)

    # Accesses year from calendar DICT
    def get_year(self, year_num):
        return self.calendar_dict[year_num]

    # Holds 12 months of data
    class Year:
        def __init__(self, year_num):
            self.year_num = year_num
            self.months_list = self.generate_year()

        # Creates a LIST to store each month
        def generate_year(self):
            year = []
            for month_num in range(1, 13):
                year.append(self.Month(self.year_num, month_num))
            return year

        # Accesses desired month
        def get_month(self, month_num):
            return self.months_list[month_num - 1]

        # Holds X days of data, where X is the number of days in the month
        class Month:
            num_to_month = {
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
                12: "December",
            }

            month_to_days = {
                "January": 31,
                "February": 28,
                "March": 31,
                "April": 30,
                "May": 31,
                "June": 30,
                "July": 31,
                "August": 31,
                "September": 30,
                "October": 31,
                "November": 30,
                "December": 31
            }

            def __init__(self, year_num, month_num):
                self.year_num = year_num
                self.month_num = month_num
                self.month_name = self.num_to_month[month_num]

                self.day_count = 0
                if self.month_name == "February" and isleap(year_num):
                    self.day_count = 29
                else:
                    self.day_count = self.month_to_days[self.month_name]

                self.days_list = self.generate_month()

            # Creates a LIST to store DailyData
            def generate_month(self):
                month = []
                for day_num in range(1, self.day_count + 1):
                    month.append(DailyData(self.year_num, self.month_num, day_num))
                return month

            # Returns DailyData
            def get_day(self, day_num):
                return self.days_list[day_num - 1]


# Holds all the entries information for each day
# Budget categories are only present for analysis purposes, not for displaying remaining amount
class DailyData:
    def __init__(self, year_num, month_num, day_num):
        self.year_num = year_num
        self.month_num = month_num
        self.day_num = day_num

    def Test(self):
        print(self.year_num, self.month_num, self.day_num)


# Main class that holds the functions for reading and writing data
class Database:
    def __init__(self):
        self.index = 0

        self.data_calendar = DataCalendar()

    def get_current_date_data(self):
        current_date = date.today()
        current_year = current_date.year
        current_month = current_date.month
        current_day = current_date.day

        return self.data_calendar.get_data(current_year, current_month, current_day)

    def Test(self):
        data = self.get_current_date_data()
        data.Test()
