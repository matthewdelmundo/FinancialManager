import re
import kivy
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

from database import convert_month_num

# Loads kv files for this screen
from kivy.lang import Builder
Builder.load_file('kv Files/homescreen.kv')

class HomeScreen(Screen):
    def __init__(self, database, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        self.database = database

        #Initialize Labels
        self.set_active_date_label()
        self.ids.home_toolbar.ids.title.text = "Home"


    # Gets the total amount from HistoryScreen
    def total_balance(self):
        total = self.database.get_all_entries_total()

        #total = self.caller_widget.get_entries_list_total()
        #budgets = budgetscreen.get_budgets_list()
        
        # positive value, green text
        if total >= 0:
            self.ids.total_balance.color = (0.47, 0.75, 0.39, 1)
            text = '₱{:,.2f}'.format(total)
            self.ids.total_balance.text = text

        # negative value, red text
        else:
            abs_total = abs(total)
            self.ids.total_balance.color = (0.75, 0.47, 0.39, 1)
            text = '-₱{:,.2f}'.format(abs_total)
            self.ids.total_balance.text = text

    def set_active_date_label(self):
        active_date = self.database.get_current_date()
        date_text = "{day} {month} {year}".format(day=active_date[0],
                                                  month=convert_month_num(active_date[1]),
                                                  year=active_date[2])
        self.ids.active_date.text = date_text