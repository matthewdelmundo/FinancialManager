from globalwidgets import *
from historyscreen import *
from budgetscreen import *
from addscreen import *
from datepicker import *
from database import *

import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

# Loads kv files used by multiple screens
from kivy.lang import Builder
Builder.load_file('kv Files/globalwidgets.kv')


# App Build
class FinancialManagerApp(App):
    def build(self):
        database = Database()
        sm = ScreenManager()
        history_screen = HistoryScreen(database, name='history')

        sm.add_widget(history_screen)
        sm.add_widget(BudgetScreen(name='budget'))
        sm.add_widget(GlobalAdd(database, history_screen, name='add'))
        return sm
    

# Run
if __name__ == "__main__":
    FinancialManagerApp().run()
