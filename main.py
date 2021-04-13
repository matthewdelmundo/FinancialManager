from globalwidgets import *
from historyscreen import *
from budgetscreen import *

import kivy
from kivy.app import App

# Loads kv files used by multiple screens
from kivy.lang import Builder
Builder.load_file('globalwidgets.kv')

from kivy.uix.screenmanager import ScreenManager, Screen

# App Build
class FinancialManagerApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(BudgetScreen(name='budget'))
        sm.add_widget(HistoryScreen(name='history'))
        return sm


# Run
if __name__ == "__main__":
    FinancialManagerApp().run()
