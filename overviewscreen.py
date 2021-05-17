import re
import kivy
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen

# Loads kv files for this screen
from kivy.lang import Builder
Builder.load_file('kv Files/overviewscreen.kv')

# Widget that shows Expense Category and the total expense
class Expense(AnchorLayout):
    def __init__(self, caller_widget, name, amount, **kwargs):
        super(Expense, self).__init__(**kwargs)
        
        self.caller_widget = caller_widget
        self.name = name
        self.amount = amount
        self.initialize_entry()

    def initialize_entry(self):
        self.ids.expense_name.text = self.name
        self.ids.expense_amount.text = self.amount


# Main screen showing spending breakdown
class OverviewScreen(Screen):
    expenses_grid = ObjectProperty(None)
    # expenses_list = []

    def __init__(self, **kwargs):
        super(OverviewScreen, self).__init__(**kwargs)

        # TODO: DEBUG (Remove in Final)
        # Sets window to phone ratio
        Window.size = (338, 600)

        # Initialize Labels
        self.ids.overview_toolbar.ids.title.text = "Overview"

        # Sets GridLayout size to its number of entries -> allows scrolling
        self.expenses_grid.bind(minimum_height=self.expenses_grid.setter("height"))

    # Updates the values of the Total Income, Total Expense, and Net Income
    def update_total_values(self, income, expense, net):
        self.ids["total_values"].ids["total_income"].text = income
        self.ids["total_values"].ids["total_expense"].text = expense
        self.ids["total_values"].ids["net_income"].text = net
        if net > 0:
            self.ids["total_values"].ids["net_income"].text_color = (0.47, 0.75, 0.39, 1)
        else: 
            self.ids["total_values"].ids["net_income"].text_color = (0.94, 0.35, 0.39, 1)

    def add_expense_category(self, name, amount):
        expense = Expense(self, name, amount)
        self.ids.expenses_grid.add_widget(expense)
        

