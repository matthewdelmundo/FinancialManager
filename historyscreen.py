import re
import kivy
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from budgetscreen import *
#from add import *

from datepicker import DatePickerButton

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



# Popup window for clicking the "Total Balance" button
class PopUpTotalBalance(Popup):
    def __init__(self, caller_widget, **kwargs):
        super(PopUpTotalBalance, self).__init__(**kwargs)

        # Widget that called this popup
        self.caller_widget = caller_widget

    # Gets the total amount from HistoryScreen
    def total_balance(self):
        total = self.caller_widget.get_entries_list_total()
        #budgets = budgetscreen.get_budgets_list()
        #print(budgets)

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

# Main screen showing entry history
# Should use array to store and edit data
class HistoryScreen(Screen):
    entries_grid = ObjectProperty(None)
    entries_list = []

    def __init__(self, database, **kwargs):
        super(HistoryScreen, self).__init__(**kwargs)

        # TODO: DEBUG (Remove in Final)
        # Sets window to phone ratio
        Window.size = (338, 600)

        self.database = database

        # Sets GridLayout size to its number of entries -> allows scrolling
        self.entries_grid.bind(minimum_height=self.entries_grid.setter("height"))

        # Reference to the popup for ease of opening
        self.total_balance_popup = PopUpTotalBalance(self)

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

    def Test(self):
        self.database.Test()