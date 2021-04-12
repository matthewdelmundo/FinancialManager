from globalwidgets import *
from historyscreen import *
from budgetscreen import *

import kivy
from kivy.app import App

# Loads kv files used by multiple screens
from kivy.lang import Builder
Builder.load_file('globalwidgets.kv')

from kivy.uix.screenmanager import ScreenManager, Screen

class WindowManager(ScreenManager):
    pass

# App Build
class FinancialManagerApp(App):
    def build(self):
        return WindowManager()


# Run
if __name__ == "__main__":
    FinancialManagerApp().run()
