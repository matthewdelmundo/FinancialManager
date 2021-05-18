from globalwidgets import *
from homescreen import *
from historyscreen import *
from budgetscreen import *
from addscreen import *
from overviewscreen import *
from datepicker import *
from database import *
from budgetdatabase import *

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
        budget_database = BudgetDatabase(database)

        sm = ScreenManager()
        home_screen = HomeScreen(database, name='home')
        history_screen = HistoryScreen(database, name='history')
        budget_screen = BudgetScreen(budget_database, name='budget')
        overview_screen = OverviewScreen(database, name='overview')
        add_screen = GlobalAdd(database, history_screen, budget_screen, name='add')

        sm.add_widget(home_screen)
        sm.add_widget(history_screen)
        sm.add_widget(budget_screen)
        sm.add_widget(overview_screen)
        sm.add_widget(add_screen)

        # Save screens
        self.sm = sm
        self.home_screen = home_screen
        self.budget_screen = budget_screen
        self.history_screen = history_screen
        self.overview_screen = overview_screen 
        self.add_screen = add_screen
        return sm
    
    def go_to_home(self):
        self.sm.switch_to(self.home_screen, direction='right')
        
    def go_to_budget(self):
        if self.sm.current == 'home':
            dir = 'left'
        else:
            dir = 'right'
        self.budget_screen.on_screen_callback()
        self.sm.switch_to(self.budget_screen, direction=dir)

    def go_to_history(self):
        if self.sm.current == 'home' or self.sm.current == 'budget':
            dir = 'left'
        else:
            dir = 'right'
        self.sm.switch_to(self.history_screen, direction=dir)

    def go_to_overview(self):
        self.overview_screen.on_screen_callback()
        self.sm.switch_to(self.overview_screen, direction='left')

    def go_to_add(self):
        self.sm.switch_to(self.add_screen, direction='left')


# Run
if __name__ == "__main__":
    FinancialManagerApp().run()
