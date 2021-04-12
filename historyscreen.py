import re
import kivy
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen

# Loads kv files for this screen
from kivy.lang import Builder
Builder.load_file('historyscreen.kv')


# Popup window for editing an entry
class PopUpEditEntryIncome(Popup):
    def __init__(self, caller_widget, **kwargs):
        super(PopUpEditEntryIncome, self).__init__(**kwargs)

        # Widget that called this popup
        self.caller_widget = caller_widget

        self.update_edit_entry_info()

    def update_edit_entry_info(self):
        self.ids.ent_type.color = (0.95, 0.98, 0.32, 1)
        self.ids.ent_type.text = "ENTRY TYPE: INCOME"

        self.ids.ent_name.text = self.caller_widget.get_entry_name()
        self.ids.ent_amt.text = self.caller_widget.get_amount()

        self.ids.ent_amt.background_color = (0.22, 0.48, 0.3, 1)
        self.ids.ent_amt.text_color = (0.47, 0.75, 0.39, 1)
        # elif self.caller_widget.get_entry_type() == "Expense":
        #     self.ids.ent_amt.background_color = (0.63, 0.22, 0.24, 1)
        #     self.ids.ent_amt.hint_text_color = (0.94, 0.35, 0.39, 1)

    def reset_inputs(self):
        self.ids.ent_amt.text = self.caller_widget.get_amount()
        self.ids.ent_name.text = self.caller_widget.get_entry_name()

    def edit_entry(self):
        if self.ids.ent_name.text == "":
            new_name = self.caller_widget.get_entry_name()
        else:
            new_name = self.ids.ent_name.text
        new_amt = self.ids.ent_amt.text
        self.caller_widget.edit_entry_info(new_name, new_amt)
        self.dismiss()


class PopUpEditEntryExpense(Popup):
    def __init__(self, caller_widget, **kwargs):
        super(PopUpEditEntryExpense, self).__init__(**kwargs)

        # Widget that called this popup
        self.caller_widget = caller_widget

        self.update_edit_entry_info()

    def update_edit_entry_info(self):
        self.ids.ent_type.color = (0.95, 0.98, 0.32, 1)
        self.ids.ent_type.text = "ENTRY TYPE: EXPENSE"

        self.ids.ent_name.text = self.caller_widget.get_entry_name()
        self.ids.ent_amt.text = self.caller_widget.get_amount()

        self.ids.ent_amt.background_color = (0.63, 0.22, 0.24, 1)
        self.ids.ent_amt.text_color = (0.94, 0.35, 0.39, 1)

    def reset_inputs(self):
        self.ids.ent_amt.text = self.caller_widget.get_amount()
        self.ids.ent_name.text = self.caller_widget.get_entry_name()

    def edit_entry(self):
        if self.ids.ent_name.text == "":
            new_name = self.caller_widget.get_entry_name()
        else:
            new_name = self.ids.ent_name.text
        new_amt = self.ids.ent_amt.text
        self.caller_widget.edit_entry_info(new_name, new_amt)
        self.dismiss()


# Popup window for clicking an entry
class PopUpClickEntry(Popup):
    def __init__(self, caller_widget, **kwargs):
        super(PopUpClickEntry, self).__init__(**kwargs)

        # Widget that called this popup
        self.caller_widget = caller_widget

        self.edit_incomeentry_popup = PopUpEditEntryIncome(caller_widget)
        self.edit_expenseentry_popup = PopUpEditEntryExpense(caller_widget)

        self.update_entry_info()

    def update_entry_info(self):
        self.ids.ent_type.color = (0.95, 0.98, 0.32, 1)
        self.ids.ent_type.text = "ENTRY TYPE: " + self.caller_widget.get_entry_type()
        self.ids.ent_name.text = self.caller_widget.get_entry_name()
        if self.caller_widget.get_entry_type() == "Income":
            self.ids.ent_amt.color = (0.47, 0.75, 0.39, 1)
        elif self.caller_widget.get_entry_type() == "Expense":
            self.ids.ent_amt.color = (0.75, 0.47, 0.39, 1)
        self.ids.ent_amt.text = "AMOUNT: " + self.caller_widget.get_amount()

    def request_edit_entry(self):
        if self.caller_widget.get_entry_type() == "Income":
            self.edit_incomeentry_popup.open()
        elif self.caller_widget.get_entry_type() == "Expense":
            self.edit_expenseentry_popup.open()
        self.dismiss()


# Popup window for clicking the "Add" button
class PopUpChooseEntry(Popup):
    def __init__(self, caller_widget, **kwargs):
        super(PopUpChooseEntry, self).__init__(**kwargs)

        # Widget that called this popup
        self.caller_widget = caller_widget

        # Reference to the popup for ease of opening
        self.add_income_popup = PopUpAddIncome(caller_widget)

        # Reference to the popup for ease of opening
        self.add_expense_popup = PopUpAddExpense(caller_widget)

    # Sends caller the add_entry function with "Income" as parameter
    def choose_income(self):
        self.add_income_popup.open()
        self.dismiss()

    # Sends caller the add_entry function with "Expense" as parameter
    def choose_expense(self):
        self.add_expense_popup.open()
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


# Popup window for clicking the "Expense" button
class PopUpAddExpense(Popup):
    def __init__(self, caller_widget, **kwargs):
        super(PopUpAddExpense, self).__init__(**kwargs)

        # Widget that called this popup
        self.caller_widget = caller_widget

    # Reinitialize input boxes
    def reset_inputs(self):
        self.ids.entry_amount.initialize_values()
        self.ids.entry_name.text = ""

    # Asks caller_widget to add entry
    def add_expense_entry(self):
        display_amount = self.ids.entry_amount.text
        name = self.ids.entry_name.text
        if display_amount != "":
            if name == "":
                name = "New Expense"
            amount = self.ids.entry_amount.get_amount()
            self.caller_widget.add_entry("Expense", name, display_amount, amount)
            self.dismiss()


# Popup window for clicking the "Total Balance" button
class PopUpTotalBalance(Popup):
    def __init__(self, caller_widget, **kwargs):
        super(PopUpTotalBalance, self).__init__(**kwargs)

        # Widget that called this popup
        self.caller_widget = caller_widget

    # Gets the total amount from HistoryScreen
    def total_balance(self):
        total = self.caller_widget.get_entries_list_total()

        # positive value, green text
        if total >= 0:
            self.ids.total_balance.color = (0.47, 0.75, 0.39, 1)
            text = '₱{:,.2f}'.format(total)
            self.ids.total_balance.text = text

        # negative value, red text
        else:
            abs_total = abs(total)
            self.ids.total_balance.color = (0.75, 0.47, 0.39, 1)
            text = '-₱{:,.2f}'.format(abs_total)
            self.ids.total_balance.text = text


# Custom TextInput for entry name
class EntryNameInput(TextInput):
    # Prevents name from going over 24 characters
    def insert_text(self, substring, from_undo=False):
        if len(self.text) >= 24:
            return
        return super(EntryNameInput, self).insert_text(substring, from_undo)


class EditNameInput(TextInput):
    # Prevents name from going over 24 characters
    def insert_text(self, substring, from_undo=False):
        if len(self.text) >= 24:
            return
        return super(EditNameInput, self).insert_text(substring, from_undo)


# Custom Widget for the entries.
# entry_type = "Income"/"Expense"
# index = index in the currently used entries_list (found in HistoryScreen)
class Entry(Widget):
    def __init__(self, entry_type, name, display_amount, index, caller_widget, **kwargs):
        super(Entry, self).__init__(**kwargs)
        self.entry_type = entry_type
        self.name = name
        self.display_amount = display_amount
        self.index = index
        self.caller_widget = caller_widget
        self.click_entry_popup = PopUpClickEntry(self)

        self.initialize_entry()

    def edit_entry_info(self, new_name, new_amt):  ###### ALERT!
        self.name = new_name
        self.ids.entry_name.text = new_name

        # if user just clicked the finish w/o changing, retain its values
        if new_amt == '':
            return
        self.display_amount = new_amt
        self.ids.entry_display_amount.text = new_amt
        self.caller_widget.update_entries_list(self.name, self.display_amount, self.index, self.entry_type)

    def get_entry_type(self):
        return self.entry_type

    def get_entry_name(self):
        return self.name

    def get_amount(self):
        return self.display_amount

    # Initializes entry for UI display
    # Turns amount font color to green when Income entry
    def initialize_entry(self):
        self.ids.entry_name.text = self.name
        self.ids.entry_display_amount.text = self.display_amount
        if self.entry_type == "Income":
            self.ids.entry_display_amount.color = (0.47, 0.75, 0.39, 1)
        elif self.entry_type == "Expense":
            self.ids.entry_display_amount.color = (0.94, 0.35, 0.39, 1)

    # Prints list index when widget is pressed
    def press(self):
        self.click_entry_popup.open()


# Main screen showing entry history
# Should use array to store and edit data
class HistoryScreen(Screen):
    entries_grid = ObjectProperty(None)
    entries_list = []

    def __init__(self, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)

        # TODO: DEBUG (Remove in Final)
        # Sets window to phone ratio
        Window.size = (338, 600)

        # # Sets GridLayout size to its number of entries -> allows scrolling
        # self.entries_grid.bind(minimum_height=self.entries_grid.setter("height"))

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
            new_entry = Entry(entry_type, name, display_amount, len(self.entries_list), self)
            self.ids["entries_grid"].add_widget(new_entry)

            self.entries_list.append([name, amount])

        elif entry_type == "Expense":
            new_entry = Entry(entry_type, name, display_amount, len(self.entries_list), self)
            self.ids["entries_grid"].add_widget(new_entry)

            self.entries_list.append([name, -1 * amount])

    # Views Total Balance
    def view_total_balance(self):
        self.total_balance_popup.open()

    # Update entries_list
    def update_entries_list(self, new_name, new_amount, index, entry_type):
        self.entries_list[index][0] = new_name

        # remove peso and commas
        trim = re.compile(r'[^\d.]+')
        new_amount = trim.sub('', new_amount)
        new_amount = float(new_amount)
        if entry_type == "Income":
            self.entries_list[index][1] = new_amount
        elif entry_type == "Expense":
            self.entries_list[index][1] = -1 * new_amount

    # Gets the sum of the entries_list
    def get_entries_list_total(self):
        total = 0
        for i in range(len(self.entries_list)):
            total = total + self.entries_list[i][1]
        return total
