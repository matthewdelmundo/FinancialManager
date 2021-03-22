import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.core.window import Window


# Popup window for clicking the "Add" button
class PopUpChooseEntry(Popup):
    def __init__(self, caller_widget, **kwargs):
        super(PopUpChooseEntry, self).__init__(**kwargs)

        # Widget that called this popup
        self.caller_widget = caller_widget

    # Sends caller the add_entry function with "Income" as parameter
    def choose_income(self):
        self.caller_widget.add_entry("Income")
        self.dismiss()

    # Sends caller the add_entry function with "Expense" as parameter
    def choose_expense(self):
        self.caller_widget.add_entry("Expense")
        self.dismiss()


# Popup window for clicking the "Total Balance" button
class PopUpTotalBalance(Popup):
    def __init__(self, **kwargs):
        super(PopUpTotalBalance, self).__init__(**kwargs)

    def total_balance(self):
        total = 999
        text = f'Your total balance is {total}'
        self.ids.total_balance.text = text


# Used on the title header of the screen. Was used for testing custom widget
class TitleLabel(Label):
    pass


# Unimplemented. Custom Widget for the entries.
# Should be clickable and have multiple labels indicating Name, Notes, and Amount
class Entry(Widget):
    def __init__(self, **kwargs):
        super(Entry, self).__init__(**kwargs)
        self.name = "New Entry"
        self.amount = 0


# Main screen showing entry history
# Should use array to store and edit data
class HistoryScreen(Widget):
    entries_display = ObjectProperty(None)
    entries_list = []

    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)

        # DEBUG (Remove in Final)
        # Sets window to phone ratio
        Window.size = (338, 600)

        # Sets GridLayout size to its number of entries -> allows scrolling
        self.entries_display.bind(minimum_height=self.entries_display.setter("height"))

        # Reference to the popup for ease of opening
        self.entry_popup = PopUpChooseEntry(self)
        self.total_balance_popup = PopUpTotalBalance()

    # Opens the ChooseEntry popup
    def request_add_entry(self):
        self.entry_popup.open()

    # Adds entry to UI display by adding a widget
    def add_entry(self, entry_type):
        self.ids["entries_display"].add_widget(Button(text=entry_type))

    # Views Total Balance
    def view_total_balance(self):
        self.total_balance_popup.open()


# App Build
class FinancialManagerApp(App):
    def build(self):
        return HistoryScreen()


# Run
if __name__ == "__main__":
    FinancialManagerApp().run()
