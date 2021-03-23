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
        self.caller_widget.add_entry("Expense", "", "", "")
        self.dismiss()


# Popup window for clicking the "Income" button
class PopUpAddIncome(Popup):
    def __init__(self, caller_widget, **kwargs):
        super(PopUpAddIncome, self).__init__(**kwargs)

        # Widget that called this popup
        self.caller_widget = caller_widget

    # Reinitialize input boxes
    def reset_inputs(self):
        self.ids.entry_amount.initialize_values()
        self.ids.entry_name.text = ""

    # Asks caller_widget to add entry
    def add_income_entry(self):
        display_amount = self.ids.entry_amount.text
        name = self.ids.entry_name.text
        if display_amount != "":
            if name == "":
                name = "New Income"
            amount = self.ids.entry_amount.get_amount()
            self.caller_widget.add_entry("Income", name, display_amount, amount)
            self.dismiss()


# Popup window for clicking the "Total Balance" button
class PopUpTotalBalance(Popup):
    def __init__(self, caller_widget, **kwargs):
        super(PopUpTotalBalance, self).__init__(**kwargs)

        # Widget that called this popup
        self.caller_widget = caller_widget

    def total_balance(self):
        total = self.caller_widget.get_entries_list_total()
        if total >= 0:
            self.ids.total_balance.color = (0.47, 0.75, 0.39, 1)
            text = f'₱{total}'
            self.ids.total_balance.text = text
        else:
            abs_total = abs(total)
            self.ids.total_balance.color = (0.75, 0.47, 0.39, 1)
            text = f'-₱{abs_total}'
            self.ids.total_balance.text = text

        



# Custom TextInput for entry name
class EntryNameInput(TextInput):
    # Prevents name from going over 24 characters
    def insert_text(self, substring, from_undo=False):
        if len(self.text) >= 24:
            return
        return super(EntryNameInput, self).insert_text(substring, from_undo)


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
        self.text = ""
        self.digits = 0
        self.pre_period_amount = ""
        self.font_size = 40

    # Retrieves float amount
    def get_amount(self):
        return float(self.pre_period_amount + self.text[-3:])

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

    # Adds '.XX' at the end of the string
    def append_zeroes(self):
        if self.text != '':
            end = self.text[-3:]
            zero_pos = end.find('.')
            if zero_pos == -1:
                self.text += '.00'
            else:
                for i in range(0, zero_pos):
                    self.text += '0'

    # Calls append_zeroes when user presses 'enter'
    def on_text_validate(self):
        self.append_zeroes()


# Custom Widget for the entries.
# entry_type = "Income"/"Expense"
# index = index in the currently used entries_list (found in HistoryScreen)
class Entry(Widget):
    def __init__(self, entry_type, name, display_amount, index, **kwargs):
        super(Entry, self).__init__(**kwargs)
        self.entry_type = entry_type
        self.name = name
        self.display_amount = display_amount
        self.index = index

        self.initialize_entry()

    # Initializes entry for UI display
    # Turns amount font color to green when Income entry
    def initialize_entry(self):
        self.ids.entry_name.text = self.name
        self.ids.entry_display_amount.text = self.display_amount
        if self.entry_type == "Income":
            self.ids.entry_display_amount.color = (0.47, 0.75, 0.39, 1)

    # Prints list index when widget is pressed
    def press(self):
        print(self.index)


# Main screen showing entry history
# Should use array to store and edit data
class HistoryScreen(Widget):
    entries_display = ObjectProperty(None)
    entries_list = []

    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)

        # TODO: DEBUG (Remove in Final)
        # Sets window to phone ratio
        Window.size = (338, 600)

        # Sets GridLayout size to its number of entries -> allows scrolling
        self.entries_display.bind(minimum_height=self.entries_display.setter("height"))

        # Reference to the popup for ease of opening
        self.entry_popup = PopUpChooseEntry(self)
        self.total_balance_popup = PopUpTotalBalance(self)

    # Opens the ChooseEntry popup
    def request_add_entry(self):
        self.entry_popup.open()

    # Adds entry to UI display by adding a widget
    # display_amount is the amount in the format ₱XX,XXX.XX
    # amount is the float amount for use in the data array
    def add_entry(self, entry_type, name, display_amount, amount):
        if entry_type == "Income":
            new_entry = Entry(entry_type, name, display_amount, len(self.entries_list))
            self.ids["entries_display"].add_widget(new_entry)

            self.entries_list.append([name, amount])
        elif entry_type == "Expense":
            self.ids["entries_display"].add_widget(Button(text=entry_type))

    # Views Total Balance
    def view_total_balance(self):
        self.total_balance_popup.open()

    def get_entries_list_total(self):
        total = 0
        for i in range(len(self.entries_list)):
            total = total + self.entries_list[i][1]
        return total



# App Build
class FinancialManagerApp(App):
    def build(self):
        return HistoryScreen()


# Run
if __name__ == "__main__":
    FinancialManagerApp().run()
