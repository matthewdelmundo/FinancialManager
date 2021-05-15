import re
import kivy
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from historyscreen import *

# Loads kv files for this screen
from kivy.lang import Builder
Builder.load_file('kv Files/addscreen.kv')


# Popup window for clicking the "Add" button
class PopUpChooseEntry(Popup):
    def __init__(self, caller_widget, **kwargs):
        super(PopUpChooseEntry, self).__init__(**kwargs)

        # Widget that called this popup
        self.caller_widget = caller_widget

        # Reference to the popup for ease of opening
        self.add_income_popup = PopUpAddIncome(caller_widget)

        # Reference to the popup for ease of opening
        self.add_expense_popup = PopUpAddExpense(caller_widget, self)

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
            self.caller_widget.add_entry("Income", name, display_amount, amount, None)

            self.dismiss()


# Popup window for clicking the "Expense" button
class PopUpAddExpense(Popup):
    def __init__(self, caller_widget, parent_widget, **kwargs):
        super(PopUpAddExpense, self).__init__(**kwargs)

        # Widget that called this popup
        self.caller_widget = caller_widget
        self.parent_widget = parent_widget

        # Reference to the popup for ease of opening
        self.select_category_popup = PopupSelectCategory(caller_widget, self)

    # Sends caller the choose_category function
    def choose_category(self):
        self.select_category_popup.open()
        self.dismiss()

    # Reinitialize input boxes
    def reset_inputs(self):
        self.ids.entry_amount.initialize_values()
        self.ids.entry_name.text = ""

    # Asks caller_widget to add entry
    def add_expense_entry(self):
        display_amount = self.ids.entry_amount.text
        name = self.ids.entry_name.text
        category = self.ids.category_name.text
        if category == "Category":
            category = ""
        if display_amount != "":
            if name == "":
                name = "New Expense"
            amount = self.ids.entry_amount.get_amount()
            self.caller_widget.add_entry("Expense", name, display_amount, amount, category)
            self.dismiss()

# Popup window for clicking the "Category" button
class PopupSelectCategory(Popup):
    categories_grid = ObjectProperty(None)
    categories_list = []
    def __init__(self, caller_widget, parent_widget, **kwargs):
        super(PopupSelectCategory, self).__init__(**kwargs)

        # Widget that called this popup
        self.caller_widget = caller_widget
        self.parent_widget = parent_widget
        
        # Sets GridLayout height to its number of entries -> allows scrolling
        self.categories_grid.bind(minimum_height=self.categories_grid.setter("height"))

    def return_to_add(self):
        # self.dismiss()
        self.parent_widget.parent_widget.choose_expense()

    def update_categories(self):
        self.ids["categories_grid"].clear_widgets()
        self.categories_list = self.caller_widget.get_budgets_list()
        new_cat = Category(self, "")
        self.ids["categories_grid"].add_widget(new_cat)
        for name in self.categories_list:
            new_cat = Category(self, name)
            self.ids["categories_grid"].add_widget(new_cat)


# Popup window for clicking an entry
class PopUpClickEntry(Popup):
    def __init__(self, caller_widget, **kwargs):
        super(PopUpClickEntry, self).__init__(**kwargs)

        # Widget that called this popup
        self.caller_widget = caller_widget

        self.edit_incomeentry_popup = PopUpEditEntryIncome(caller_widget)
        self.edit_expenseentry_popup = PopUpEditEntryExpense(caller_widget, self)

        self.req_del_entry = PopUpDeleteEntry(caller_widget)

        self.update_entry_info()
    
    def request_del_entry(self):
        self.req_del_entry.open()

    def update_entry_info(self):
        self.ids.ent_type.color = (0.95, 0.98, 0.32, 1)
        self.ids.ent_type.text = "ENTRY TYPE: " + self.caller_widget.get_entry_type()
        self.ids.ent_name.text = self.caller_widget.get_entry_name()
        if self.caller_widget.get_entry_type() == "Income":
            self.ids.ent_amt.color = (0.47, 0.75, 0.39, 1)
        elif self.caller_widget.get_entry_type() == "Expense":
            self.ids.ent_amt.color = (0.75, 0.47, 0.39, 1)
        self.ids.ent_amt.text = "AMOUNT: " + self.caller_widget.get_amount()
        if self.caller_widget.get_category() == None:
            category = ""
        else:
            category = self.caller_widget.get_category()
        self.ids.category_name.text = "CATEGORY: " + category

    def request_edit_entry(self):
        if self.caller_widget.get_entry_type() == "Income":
            self.edit_incomeentry_popup.open()
        elif self.caller_widget.get_entry_type() == "Expense":
            self.edit_expenseentry_popup.open()
        self.dismiss()

# Custom Widget for the entries.
# entry_type = "Income"/"Expense"
# index = index in the currently used entries_list (found in HistoryScreen)
class Entry(Widget):
    def __init__(self, entry_type, name, display_amount, category, index, caller_widget, **kwargs):
        super(Entry, self).__init__(**kwargs)
        self.entry_type = entry_type
        self.name = name
        self.display_amount = display_amount
        self.category = category
        self.index = index
        self.caller_widget = caller_widget
        self.click_entry_popup = PopUpClickEntry(self)

        self.initialize_entry()

    def edit_entry_info(self, new_name, new_amt, new_cat):  ###### ALERT!
        self.name = new_name
        self.ids.entry_name.text = new_name

        # if user just clicked the finish w/o changing, retain its values
        if new_amt == '':
            return
        self.display_amount = new_amt
        self.ids.entry_display_amount.text = new_amt
        self.category = new_cat
        self.caller_widget.update_entries_list(self.name, self.display_amount, self.category, self.index, self.entry_type)

    def get_entry_type(self):
        return self.entry_type

    def get_entry_name(self):
        return self.name

    def get_amount(self):
        return self.display_amount

    def get_category(self):
        return self.category
    
    def get_index(self):
        return self.index
    
    def delete_entry_via_index(self, index):
        self.caller_widget.del_ent_via_ind(index, self)

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

class GlobalAdd(Screen):
    def __init__(self, database, history_screen, budget_screen, **kwargs):
        super(GlobalAdd, self).__init__(**kwargs)
        self.history_screen = history_screen
        self.budget_screen = budget_screen
        self.database = database
        self.entry_popup = PopUpChooseEntry(self)

        self.history_screen.set_references(self)
        self.history_screen.read_database()

    # Opens the ChooseEntry popup
    def request_add_entry(self):
        self.entry_popup.open()

    # Gets the budgets_list from budget_screen
    def get_budgets_list(self):
        return self.budget_screen.get_budgets_list()

    def edit_budget_balance(self, balance, dispbalance):
        budget_sreen = self.budget_screen
        budget_sreen.edit_budget_info(bs.new_name, balance, dispbalance)
    
    def get_entries_list(self):
        return self.history_screen.entries_list
    
    def del_ent_via_ind(self, index, entry):
        self.history_screen.entries_list.pop(index)
        self.database.delete_ent_from_db(index) 
        self.history_screen.ids["entries_grid"].remove_widget(entry)    

    # Adds entry to UI display by adding a widget
    # display_amount is the amount in the format ₱XX,XXX.XX
    # amount is the float amount for use in the data array
    def add_entry(self, entry_type, name, display_amount, amount, category, update_callback=True):
        new_entry = Entry(entry_type, name, display_amount, category,
                          len(self.history_screen.entries_list), self)

        self.history_screen.ids["entries_grid"].add_widget(new_entry)
        self.history_screen.entries_list.append([name, entry_type, category, amount])

        if update_callback:
            self.history_screen.on_entries_list_updated_callback()

    # Used when finishing edits of an entry
    def update_entries_list(self, new_name, new_amount, new_category, index, entry_type):
        print("update", self.history_screen.entries_list)
        self.history_screen.entries_list[index][0] = new_name
        self.history_screen.entries_list[index][2] = new_category

        # remove peso and commas
        trim = re.compile(r'[^\d.]+')
        new_amount = trim.sub('', new_amount)
        new_amount = float(new_amount)

        if entry_type == "Income":
            self.history_screen.entries_list[index][3] = new_amount
        elif entry_type == "Expense":
            self.history_screen.entries_list[index][3] = -1 * new_amount

        self.history_screen.on_entries_list_updated_callback()
