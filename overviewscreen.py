import re
import kivy
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen

from database import convert_month_num

# Loads kv files for this screen
from kivy.lang import Builder
Builder.load_file('kv Files/overviewscreen.kv')


# Widget that shows Expense Category and the total expense
class ExpenseSummary(RelativeLayout):
    def __init__(self, window_size, layout_size_hint, expenses_list, **kwargs):
        super(ExpenseSummary, self).__init__(**kwargs)

        self.expenses_list = expenses_list

        self.expense_info_height_hint = 0.08

        # Add widgets to stack
        expense_summary_title = ExpenseSummaryTitle(window_size, layout_size_hint,
                                                    self.expense_info_height_hint)
        self.ids["summary_grid"].add_widget(expense_summary_title)
        self.initialize_expense_summary(window_size, layout_size_hint)
        self.set_layout_size(window_size, layout_size_hint)

    def initialize_expense_summary(self, window_size, layout_size_hint):
        for expense in self.expenses_list:
            expense_info = ExpenseInfo(window_size, layout_size_hint,
                                       self.expense_info_height_hint,
                                       expense[0], expense[1])

            self.ids["summary_grid"].add_widget(expense_info)

    def set_layout_size(self, window_size, layout_size_hint):
        expense_count = len(self.expenses_list)
        height_ratio = (expense_count + 1) * self.expense_info_height_hint

        self.size = (layout_size_hint[0] * window_size[0],
                     layout_size_hint[1] * window_size[1] * height_ratio)


class ExpenseSummaryTitle(RelativeLayout):
    def __init__(self, window_size, layout_size_hint, height_hint, **kwargs):
        super(ExpenseSummaryTitle, self).__init__(**kwargs)

        self.size = (layout_size_hint[0] * window_size[0],
                     layout_size_hint[1] * window_size[1] * height_hint)


class ExpenseInfo(RelativeLayout):
    def __init__(self, window_size, layout_size_hint, height_hint,
                 name, amount, **kwargs):
        super(ExpenseInfo, self).__init__(**kwargs)

        self.size = (layout_size_hint[0] * window_size[0],
                     layout_size_hint[1] * window_size[1] * height_hint)

        self.name = name
        self.amount = '₱' + f"{amount:,.2f}"
        self.set_values(self.name, self.amount)

    def set_values(self, name, amount):
        self.ids["expense_name"].text = name
        self.ids["expense_amount"].text = amount


class TotalValues(RelativeLayout):
    def __init__(self, window_size, layout_size_hint, total_values, **kwargs):
        super(TotalValues, self).__init__(**kwargs)

        self.size = (layout_size_hint[0] * window_size[0],
                     layout_size_hint[1] * window_size[1] * 0.25)

        self.update_total_values(total_values)

    # Updates the values of the Total Income, Total Expense, and Net Income
    def update_total_values(self, total_values):
        income = total_values[0]
        expense = total_values[1]
        net = income - expense

        self.ids["total_income"].text = '₱' + f"{income:,.2f}"
        self.ids["total_expense"].text =  '₱' + f"{expense:,.2f}"

        self.ids["net_income"].color = (0.47, 0.75, 0.39, 1)
        self.ids["net_income"].text = '₱' + f"{abs(net):,.2f}"
        if net < 0:
            self.ids["net_income"].color = (0.94, 0.35, 0.39, 1)


# Main screen showing spending breakdown
class OverviewScreen(Screen):
    overviews_grid = ObjectProperty(None)
    # expenses_list = []

    def __init__(self, database, **kwargs):
        super(OverviewScreen, self).__init__(**kwargs)

        # TODO: DEBUG (Remove in Final)
        # Sets window to phone ratio
        Window.size = (338, 600)

        self.database = database
        self.active_date = self.database.get_current_date()

        self.overviews_grid.bind(minimum_height=self.overviews_grid.setter("height"))

        # Initialize Labels
        self.ids["overview_toolbar"].ids["title"].text = "Overview"

        self.reinitialize_screen()

    def on_screen_callback(self):
        self.reinitialize_screen()

    def reinitialize_screen(self):
        self.set_active_date_label()

        # Get Data
        total_values = self.get_total_values()
        expenses_list = self.get_expenses_list()

        self.ids["overviews_grid"].clear_widgets()

        # Add Widgets
        self.add_total_values(total_values)
        self.add_expense_summary(expenses_list)

    def set_active_date_label(self):
        self.active_date = self.database.get_current_date()
        date_text = "{day} {month} {year}".format(day=self.active_date[0],
                                                  month=convert_month_num(self.active_date[1]),
                                                  year=self.active_date[2])
        self.ids["active_date"].text = date_text

    def get_total_values(self):
        total_income = self.database.get_total_income(self.active_date)
        total_expense = self.database.get_total_expense(self.active_date)
        return total_income, total_expense

    def get_expenses_list(self):
        return self.database.get_expense_categories_list(self.active_date)

    def add_total_values(self, total_values):
        total_values_widget = TotalValues(Window.size, (0.7, 0.73), total_values)
        self.ids["overviews_grid"].add_widget(total_values_widget)

    def add_expense_summary(self, expenses_list):
        if len(expenses_list) == 0:
            return
        expense_summary = ExpenseSummary(Window.size, (0.7, 0.73),
                                         expenses_list)
        self.ids["overviews_grid"].add_widget(expense_summary)