import kivy
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout

# Loads kv files for this screen
from kivy.lang import Builder
Builder.load_file('budgetscreen.kv')


class PopupAddBudget(Popup):
    def __init__(self, caller_widget, **kwargs):
        super(PopupAddBudget, self).__init__(**kwargs)

        # Widget that called this popup
        self.caller_widget = caller_widget


class Budget(AnchorLayout):
    def __init__(self, **kwargs):
        super(Budget, self).__init__(**kwargs)


class AddBudgetButton(AnchorLayout):
    caller_widget = None

    # Manually sets caller widget
    def set_caller_widget(self, caller_widget):
        self.caller_widget = caller_widget

    def button_function(self):
        self.caller_widget.popup_add_budget()


class BudgetScreen(Widget):
    budgets_grid = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(BudgetScreen, self).__init__(**kwargs)

        # TODO: DEBUG (Remove in Final)
        # Sets window to phone ratio
        Window.size = (338, 600)

        # Sets GridLayout height to its number of entries -> allows scrolling
        self.budgets_grid.bind(minimum_height=self.budgets_grid.setter("height"))

        # Initialize Labels
        self.ids["budgets_toolbar"].ids["title"].text = "Budgets"

        # Set called widget
        self.ids["add_budget_button"].set_caller_widget(self)

    def popup_add_budget(self):
        print("Add Budget")

    def pressed(self):
        print("Hello World!")

    def pressed2(self):
        print("Hello World!2")
