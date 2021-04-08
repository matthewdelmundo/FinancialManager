from historyscreen import *
from budgetscreen import *

import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.properties import ColorProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

# Loads kv files used by multiple screens
from kivy.lang import Builder
Builder.load_file('global.kv')


# TODO: might delete
class CircularButton(Button):
    color = ColorProperty()

    def button_pressed(self):
        self.color = self.bg_color_down

    def button_released(self):
        self.color = self.bg_color_normal


# TODO: might delete
class RoundedButton(Button):
    color = ColorProperty()

    def button_pressed(self):
        self.color = self.bg_color_down

    def button_released(self):
        self.color = self.bg_color_normal

# TODO: Use this for custom buttons
class ImageButton(Button):
    def button_pressed(self):
        self.source = self.image_down

    def button_released(self):
        self.source = self.image_normal


# App Build
class FinancialManagerApp(App):
    def build(self):
        return BudgetScreen()


# Run
if __name__ == "__main__":
    FinancialManagerApp().run()
