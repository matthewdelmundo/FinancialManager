import re
import kivy
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen

from budgetscreen import *
from database import create_entry_dict
from database import convert_month_num

# Loads kv files for this screen
from kivy.lang import Builder
Builder.load_file('kv Files/historyscreen.kv')

class PopUpDeleteEntry(Popup):
    def __init__(self, caller_widget, immediate_caller_widget, **kwargs):
        super(PopUpDeleteEntry, self).__init__(**kwargs)

        # Widget that called this popup
        self.caller_widget = caller_widget
        self.immediate_caller_widget = immediate_caller_widget

    def delete_entry(self):
        ent_ind = self.caller_widget.get_index()
        self.caller_widget.delete_entry_via_index(ent_ind)
        self.dismiss()
        self.immediate_caller_widget.return_to_edit_pop()
    
    def return_to_edit(self):
        self.dismiss()

# Popup window for editing an entry
class PopUpEditEntryIncome(Popup):
    def __init__(self, caller_widget, **kwargs):
        super(PopUpEditEntryIncome, self).__init__(**kwargs)

        # Widget that called this popup
        self.caller_widget = caller_widget
        self.req_del_ent = PopUpDeleteEntry(caller_widget, self)
 
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
        self.caller_widget.edit_entry_info(new_name, new_amt, None)
        self.dismiss()

    def request_del_entry(self):
        self.req_del_ent.open()
        
    def return_to_edit_pop(self):
        self.dismiss()
        
class PopUpEditEntryExpense(Popup):
    def __init__(self, caller_widget, parent_widget, **kwargs):
        super(PopUpEditEntryExpense, self).__init__(**kwargs)

        # Widget that called this popup
        self.caller_widget = caller_widget
        self.parent_widget = parent_widget

        self.req_del_ent = PopUpDeleteEntry(caller_widget, self)
        self.update_edit_entry_info()

        self.select_category_popup = PopupEditCategory(caller_widget, self)

    # Sends caller the select_category function with "Expense" as parameter
    def choose_category(self):
        self.select_category_popup.open()

    def update_edit_entry_info(self):
        self.ids.ent_type.color = (0.95, 0.98, 0.32, 1)
        self.ids.ent_type.text = "ENTRY TYPE: EXPENSE"

        self.ids.ent_name.text = self.caller_widget.get_entry_name()
        self.ids.ent_amt.text = self.caller_widget.get_amount()

        if self.caller_widget.get_category() == "":
            self.ids.category_name.text = "Choose Category"
        else:
            self.ids.category_name.text = self.caller_widget.get_category()

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
        if self.ids.category_name.text == "Choose Category":
            new_cat = ""
        else:
            new_cat = self.ids.category_name.text
        self.caller_widget.edit_entry_info(new_name, new_amt, new_cat)
        self.dismiss()

    def request_del_entry(self):
        self.req_del_ent.open()

    def return_to_edit_pop(self):
        self.dismiss()

# Popup window for clicking the "Category" button
class PopupEditCategory(Popup):
    def __init__(self, caller_widget, parent_widget, **kwargs):
        super(PopupEditCategory, self).__init__(**kwargs)

        # Widget that called this popup
        self.caller_widget = caller_widget
        self.parent_widget = parent_widget
        
        # Sets GridLayout height to its number of entries -> allows scrolling
        self.categories_grid.bind(minimum_height=self.categories_grid.setter("height"))

    def update_categories(self):
        self.ids["categories_grid"].clear_widgets()
        self.categories_list = self.caller_widget.get_budgets_list()
        new_cat = Category(self, "")
        self.ids["categories_grid"].add_widget(new_cat)
        for name in self.categories_list:
            new_cat = Category(self, name)
            self.ids["categories_grid"].add_widget(new_cat)


# Button/Image that lets you view the category
class Category(AnchorLayout):
    def __init__(self, caller_widget, name, **kwargs):
        super(Category, self).__init__(**kwargs)

        self.caller_widget = caller_widget
        self.name = name
        self.initialize_entry()
    def initialize_entry(self):
        self.ids.category_name.text = self.name
    def press(self):
        if self.name == '':
            self.caller_widget.parent_widget.ids.category_name.text = "Choose Category"
        else:
            self.caller_widget.parent_widget.ids.category_name.text = self.name
        self.caller_widget.dismiss()
    

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
        self.global_add = None

        # Sets GridLayout size to its number of entries -> allows scrolling
        self.entries_grid.bind(minimum_height=self.entries_grid.setter("height"))

        # Initialize Labels
        self.ids["budgets_toolbar"].ids["title"].text = "History"
        self.set_active_date_label()

        # Configures Calendar Button
        self.ids["date_picker"].set_references(self.database, self)

    # Run by GlobalAdd
    def set_references(self, global_add):
        self.global_add = global_add

    # Sets entries_grid to match data from database
    # Uses database's current date
    def read_database(self):
        new_entries_list = self.database.load_entries_list()
        for i in range(len(new_entries_list)):
            entry = new_entries_list[i]
            entry_name = entry[0]
            entry_type = entry[1]
            entry_category = entry[2]
            entry_amount = entry[3]

            display_amount = '₱{:,.2f}'.format(abs(entry_amount))
            self.global_add.add_entry(entry_type, entry_name, display_amount, entry_amount,
                                      entry_category, update_callback=False)

    # Run by DatePickerButton
    # Reads database after date has been change
    def on_date_change_callback(self):
        self.set_active_date_label()

        self.ids["entries_grid"].clear_widgets()
        self.entries_list = []
        self.read_database()

    def set_active_date_label(self):
        active_date = self.database.get_current_date()
        date_text = "{day} {month} {year}".format(day=active_date[0],
                                                  month=convert_month_num(active_date[1]),
                                                  year=active_date[2])
        self.ids["active_date"].text = date_text

    # Run every time the current entries_list is updated
    def on_entries_list_updated_callback(self):
        entry_dict_list = []
        # Converts entries_list to dict compatible with data storage
        for i in range(len(self.entries_list)):
            entry = self.entries_list[i]
            entry_name = entry[0]
            entry_type = entry[1]
            entry_category = entry[2]
            entry_amount = entry[3]

            entry_dict = create_entry_dict(entry_name, entry_type,
                                           entry_category, entry_amount)
            entry_dict_list.append(entry_dict)

        self.database.save_entries_list(entry_dict_list)

    def clear_entries(self):
        self.ids["entries_grid"].clear_widgets()
        self.entries_list = []
        self.database.delete_entries_list()

