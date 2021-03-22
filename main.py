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

        # Reference to the popup for ease of opening
        self.add_income_popup = PopUpAddIncome(caller_widget)

    # Sends caller the add_entry function with "Income" as parameter
    def choose_income(self):
        self.add_income_popup.open()
        self.dismiss()

    # Sends caller the add_entry function with "Expense" as parameter
    def choose_expense(self):
        self.caller_widget.add_entry("Expense")
        self.dismiss()


# Popup window for clicking the "Income" button
class PopUpAddIncome(Popup):
    def __init__(self, caller_widget, **kwargs):
        super(PopUpAddIncome, self).__init__(**kwargs)

        # Widget that called this popup
        self.caller_widget = caller_widget

    def reset_inputs(self):
        self.ids.entry_amount.initialize_values()

        # TODO: RESET ALL INPUT BOXES AFTER ON_DISMISS


# Popup window for clicking the "Total Balance" button
class PopUpTotalBalance(Popup):
    def __init__(self, **kwargs):
        super(PopUpTotalBalance, self).__init__(**kwargs)

    def total_balance(self):
        total = 999
        text = f'Your total balance is {total}'
        self.ids.total_balance.text = text


# Custom TextInput for entries
class AmountInput(TextInput):
    def __init__(self, **kwargs):
        super(AmountInput, self).__init__(**kwargs)
        # Counts only digits before a period
        self.number_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.digits_to_font_size = {
            5: 40,
            6: 36,
            7: 32,
            8: 28,
            9: 26,
        }
        self.digits = 0
        self.pre_period_amount = ""

    def initialize_values(self):
        self.digits = 0
        self.pre_period_amount = ""
        self.text = ""

    # Input validation for backspaces
    def do_backspace(self, from_undo=False, mode='bkspc'):
        if '.' not in self.text:
            # Reduces digit count if about-to-be-erased character is a digit
            if len(self.text) > 0 and self.text[self.cursor_index()-1] in self.number_list:
                self.digits -= 1
            # Deletes last digit of the pre-period amount
            self.pre_period_amount = self.pre_period_amount[:-1]
            self.add_commas_to_display('delete')
            # Removes '₱' character when erasing there are no digits left
            if self.digits == 0:
                self.text = ''
            self.adjust_font_size()
        return super(AmountInput, self).do_backspace(from_undo, mode)

    # Input validation for the format ₱XX,XXX.XX
    def insert_text(self, substring, from_undo=False):
        # Only allows input of numbers and a period
        if substring not in self.number_list + ['.']:
            return
        # Makes sure there is only 1 period and that there is a max of 2 digits after period
        if '.' in self.text:
            dot_index = self.text.find('.')
            if substring == '.' or len(self.text[dot_index:]) > 2:
                return
        else:
            # Does not allow amount to start with a 0 or '.'
            if self.digits == 0 and (substring == '0' or substring == '.'):
                return
            # If input is a number
            if substring != '.':
                # Max number of pre-period digits = 9
                if self.digits >= 9:
                    return
                # Adds to digit count
                self.digits += 1
                # Adds the digit to the pre-period amount
                self.pre_period_amount += substring
                self.add_commas_to_display('insert')
                self.adjust_font_size()
        return super(AmountInput, self).insert_text(substring, from_undo)

    # Changes the font size according to how many digits are in the text
    def adjust_font_size(self):
        if self.digits >= 5:
            self.font_size = self.digits_to_font_size[self.digits]

    # Magically adds commas to the pre-period digits
    def add_commas_to_display(self, mode):
        new_pre_period = ''
        count = 0
        for i in range(len(self.pre_period_amount) - 1, -1, -1):
            count += 1
            new_pre_period = self.pre_period_amount[i] + new_pre_period
            if count % 3 == 0 and i - 1 != -1:
                new_pre_period = ',' + new_pre_period
        if mode == 'insert':
            self.text = '₱' + new_pre_period[:-1]
        else:
            self.text = '₱' + new_pre_period + '0'


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
        pass
        ### self.add_entry_popup.open()
        ### self.ids["entries_display"].add_widget(Button(text=entry_type))

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
