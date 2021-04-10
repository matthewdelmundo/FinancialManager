import kivy
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout

# Loads kv files for this screen
from kivy.lang import Builder
Builder.load_file('budgetscreen.kv')


# Popup for choosing a new icon for budget
class PopupChooseIcon(Popup):
    icon_grid = ObjectProperty(None)

    icon_sources = [
        "images/temp/icons/expense/food.png",
        "images/temp/icons/expense/game.png",
        "images/temp/icons/expense/groceries.png",
        "images/temp/icons/expense/movies.png",
        "images/temp/icons/expense/transportation.png"
    ]

    def __init__(self, caller_widget, **kwargs):
        super(PopupChooseIcon, self).__init__(**kwargs)

        # Widget that called this popup
        self.caller_widget = caller_widget

        self.fill_icons()

    # Function that fills ui grid with icons
    def fill_icons(self):
        for source in self.icon_sources:
            icon = BudgetIcon(self, source)
            self.icon_grid.add_widget(icon)

    def pass_source(self, icon_source):
        self.caller_widget.set_icon(icon_source)
        self.dismiss()


# Button/Image that holds the icon image information
class BudgetIcon(AnchorLayout):
    def __init__(self, caller_widget, icon_source, **kwargs):
        super(BudgetIcon, self).__init__(**kwargs)

        # Widget that called this popup
        self.caller_widget = caller_widget

        # Change icon
        self.icon_source = icon_source
        self.ids["icon"].source = icon_source

    def button_function(self):
        self.caller_widget.pass_source(self.icon_source)


# Popup that lets you set budget icon, budget name, and budget amount
class PopupAddBudget(Popup):
    # Default icon in case no new icon has been set
    icon_source = "images/ui/wallet.png"

    def __init__(self, caller_widget, **kwargs):
        super(PopupAddBudget, self).__init__(**kwargs)

        # Widget that called this popup
        self.caller_widget = caller_widget

        # Popup reference
        self.choose_icon_popup = PopupChooseIcon(self)

    def reset_inputs(self):
        self.ids["budget_amount"].initialize_values()
        self.ids["budget_name"].text = ""
        self.set_icon("images/ui/wallet.png")

    def choose_icon(self):
        self.choose_icon_popup.open()

    def set_icon(self, icon_source):
        self.icon_source = icon_source
        self.ids["choose_icon"].ids["icon"].source = icon_source

    def add_budget(self):
        display_amount = "₱" + self.ids["budget_amount"].text
        amount = self.ids["budget_amount"].get_amount()
        name = self.ids["budget_name"].text
        if name == "":
            name = "New Budget"
        self.caller_widget.add_budget(name, display_amount, amount, self.icon_source)
        self.dismiss()


# Button/Image that opens the ChooseIcon popup
# Also displays current icon
class ChooseIcon(AnchorLayout):
    caller_widget = ObjectProperty(None)

    def button_function(self):
        self.caller_widget.choose_icon()


# Button/Image that opens the AddBudget popup
class AddBudgetButton(AnchorLayout):
    caller_widget = ObjectProperty(None)

    def button_function(self):
        self.caller_widget.popup_add_budget()


# Button/Image that lets you view the budget
class Budget(AnchorLayout):
    def __init__(self, caller_widget, name, display_amount, amount, icon_source, **kwargs):
        super(Budget, self).__init__(**kwargs)

        self.caller_widget = caller_widget

        # Initial values
        self.name = name
        self.display_total = display_amount
        self.total = amount
        self.icon_source = icon_source
        self.set_icon(icon_source)

        # Saved remaining amount
        self.display_remaining = display_amount
        self.remaining = amount

    def set_icon(self, icon_source):
        self.icon_source = icon_source
        self.ids["icon"].source = icon_source

    def button_function(self):
        print("Hi")
        self.caller_widget.view_budget(self.name, self.display_remaining, self.display_total)


# Budget Screen
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

        # Reference to popups
        self.add_budget_popup = PopupAddBudget(self)

    def popup_add_budget(self):
        self.add_budget_popup.open()

    def add_budget(self, name, display_amount, amount, icon_source):
        budget = Budget(self, name, display_amount, amount, icon_source)
        self.ids["budgets_grid"].add_widget(budget)

    def view_budget(self, budget_name, budget_remaining, budget_total):
        print("Hello")
        self.ids["budget_display"].ids["budget_name"].text = budget_name
        self.ids["budget_display"].ids["budget_remaining"].text = budget_remaining
        self.ids["budget_display"].ids["budget_total"].text = budget_total
