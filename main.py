from globalwidgets import *
from historyscreen import *
from budgetscreen import *

import kivy
from kivy.app import App

# Loads kv files used by multiple screens
from kivy.lang import Builder
Builder.load_file('globalwidgets.kv')


# App Build
class FinancialManagerApp(App):
    def build(self):
        return BudgetScreen()


# Run
if __name__ == "__main__":
    FinancialManagerApp().run()
