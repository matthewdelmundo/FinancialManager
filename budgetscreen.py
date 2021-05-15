import kivy
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen

from database import convert_month_num

# Loads kv files for this screen
from kivy.lang import Builder
Builder.load_file('kv Files/budgetscreen.kv')

class PopupDeleteBudget(Popup):
    def __init__(self, caller_widget, immediate_caller_widget, **kwargs):
        super(PopupDeleteBudget, self).__init__(**kwargs)

        #Budget Screen
        self.caller_widget = caller_widget

        #PopupEditBudget
        self.immediate_caller_widget = immediate_caller_widget

    #Deletes a budget
    def delete_budget(self):
        budget_names = self.caller_widget.get_budgets_list()
        if self.caller_widget.current_budget.name in budget_names:
            budget_names.remove(self.caller_widget.current_budget.name)
            self.caller_widget.ids["budgets_grid"].remove_widget(self.caller_widget.current_budget)
            self.caller_widget.budget_database.remove_budget(self.caller_widget.current_budget.name)
        self.dismiss()
        self.immediate_caller_widget.return_to_budgets_screen()

    #Called when No is pressed when asked to delete budget
    def return_to_edit(self):
        self.dismiss()

    

class PopupEditBudget(Popup):
    def __init__(self, caller_widget, **kwargs):
        super(PopupEditBudget, self).__init__(**kwargs)

        # Widget that called this popup
        self.caller_widget = caller_widget        
        self.choose_icon_popup = PopupChooseIcon(self)
        self.req_del_budget = PopupDeleteBudget(caller_widget,self)

        self.show_budget_info()
    
    def choose_icon(self):
        self.choose_icon_popup.open() 
    
    def set_icon(self, icon_source):
        self.icon_source = icon_source
        self.ids.choose_new_icon.ids.icon.source = icon_source

    def reset_inputs(self):
        self.ids.budg_name.text = self.caller_widget.current_budget.get_budg_name()
        self.ids.budg_amt.text = self.caller_widget.current_budget.get_str_budg_amt()
        self.ids.choose_new_icon.ids.icon.source = self.caller_widget.current_budget.get_budg_icon()
        self.icon_source = self.icon_source = self.caller_widget.current_budget.get_budg_icon()

    def show_budget_info(self):
        if self.caller_widget.current_budget == None:
            return                  
        self.ids.budg_name.text = self.caller_widget.current_budget.get_budg_name()
        self.ids.budg_amt.text =  self.caller_widget.current_budget.get_str_budg_amt()
        self.ids.choose_new_icon.ids.icon.source = self.caller_widget.current_budget.get_budg_icon()
        self.icon_source = self.caller_widget.current_budget.get_budg_icon()

    def edit_budget(self):
        budget_names = self.caller_widget.get_budgets_list()
        name = self.ids.budg_name.text
        if name == "" or name in budget_names:
            new_name = self.caller_widget.current_budget.get_budg_name()
        else:
            new_name = self.ids.budg_name.text
            budget_names.append(new_name)
            budget_names.remove(self.caller_widget.current_budget.get_budg_name())
        
        if self.ids.budg_amt.text == "":
            new_amt = self.caller_widget.current_budget.get_str_budg_amt()
            new_dispamt = "₱" + new_amt
        else:
            new_amt = self.ids.budg_amt.text 
            new_dispamt = "₱" + new_amt

        new_amt = float(new_amt.replace(',', ''))

        self.caller_widget.finish_edits(new_name, new_amt, new_dispamt, self.icon_source)
        self.caller_widget.update_icon(self.icon_source)
        self.dismiss()

    def request_del_budget(self):
        self.req_del_budget.open()

    def return_to_budgets_screen(self):
        self.dismiss()


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
        name = self.ids["budget_name"].text
        #display_amount = "₱" + self.ids["budget_amount"].text
        amount = self.ids["budget_amount"].get_amount()
        budget_names = self.caller_widget.get_budgets_list()

        #does not allow budgets with no names (and no amount)
        if name == "":
            self.ids.budget_name.hint_text = "field required"
            self.ids.budget_name.hint_text_color = (0.75, 0.47, 0.39, 1)
            if amount == 0:
                self.ids.budget_amount.hint_text = "field required"
                self.ids.budget_amount.hint_text_color = (0.75, 0.47, 0.39, 1)
                return
            return

        #does not allow budgets with no amounts (and no name)
        if amount == 0:
            self.ids.budget_amount.hint_text = "field required"
            self.ids.budget_amount.hint_text_color = (0.75, 0.47, 0.39, 1)
            if name == "":
                self.ids.budget_name.hint_text = "field required"
                self.ids.budget_name.hint_text_color = (0.75, 0.47, 0.39, 1)
                return
            return

        #does not allow repeating budget names (and no amount)
        if name in budget_names:
            self.ids.budget_name.text = ""
            self.ids.budget_name.hint_text = "name already exists"
            self.ids.budget_name.hint_text_color = (0.75, 0.47, 0.39, 1)
            if amount == 0:
                self.ids.budget_amount.hint_text = "field required"
                self.ids.budget_amount.hint_text_color = (0.75, 0.47, 0.39, 1)
                return
            return

        #reset default values
        self.ids.budget_name.hint_text = "Budget Name"
        self.ids.budget_name.hint_text_color = (0.5, 0.5, 0.5, 1)

        self.ids.budget_amount.hint_text = "Amount"
        self.ids.budget_amount.hint_text_color = (0.5, 0.5, 0.5, 1)

        self.caller_widget.add_budget(name, amount, self.icon_source)
        self.dismiss()

# Button/Image that opens the ChooseIcon popup
# Also displays current icon
class ChooseNewIcon(AnchorLayout):
    caller_widget = ObjectProperty(None)

    def button_function(self):
        self.caller_widget.choose_icon()

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
    def __init__(self, caller_widget, grid_index, name,
                 display_amount, amount, icon_source, **kwargs):
        super(Budget, self).__init__(**kwargs)

        self.caller_widget = caller_widget

        # Initial values
        self.name = name
        self.display_total = display_amount
        self.total = amount
        self.icon_source = icon_source
        self.set_icon(icon_source)

        self.grid_index = grid_index

        # Saved remaining amount
        self.remaining = amount

        #percentage indicates background color
        percent = (self.remaining/self.total)*100
        if percent <= 100 and percent >= 50:
            self.ids.background.background_normal = "images/ui/green.png"
        elif percent < 50 and percent >= 25:
            self.ids.background.background_normal = "images/ui/yellow.png"
        elif percent < 25 and percent >= 0:
            self.ids.background.background_normal = "images/ui/red.png"
    
    def get_budg_name(self):
        return self.name

    def get_str_budg_amt(self):
        no_peso_display_total = self.display_total[1:]
        return no_peso_display_total

    def get_budg_amt(self):
        return self.total
    
    def get_budg_icon(self):
        return self.icon_source

    def edit_budget_info(self, new_name, new_amt, new_dispamt):
        self.name = new_name
        self.total = new_amt 

        # Saved remaining amount
        self.remaining = new_amt

        # self.icon_source = new_icon_source
        # self.set_icon(icon_source)

    def set_icon(self, icon_source):
        self.icon_source = icon_source
        self.ids["icon"].source = icon_source

    #############################
    def button_function(self):
        self.caller_widget.view_budget(self)
        self.caller_widget.edit_budget_popup.show_budget_info()


# Budget Screen
class BudgetScreen(Screen):
    budgets_grid = ObjectProperty(None)
    budgets_list = []
  
    def __init__(self, budget_database, **kwargs):
        super(BudgetScreen, self).__init__(**kwargs)
        self.current_budget = None

        # TODO: DEBUG (Remove in Final)
        # Sets window to phone ratio
        Window.size = (338, 600)

        self.budget_database = budget_database

        # Sets GridLayout height to its number of entries -> allows scrolling
        self.budgets_grid.bind(minimum_height=self.budgets_grid.setter("height"))

        # Initialize Labels
        self.ids["budgets_toolbar"].ids["title"].text = "Budgets"
        self.set_active_date_label()

        # Reference to popups
        self.add_budget_popup = PopupAddBudget(self)
        self.edit_budget_popup = PopupEditBudget(self)

        self.grid_index = 1
        self.read_budget_database()

    def read_budget_database(self):
        budgets = self.budget_database.load_budgets()
        for i in range(len(budgets)):
            budget = budgets[i]
            budget_name = budget[0]
            budget_total = budget[1]
            budget_source = budget[2]

            self.add_budget(budget_name, budget_total,
                            budget_source, update_budgets=False)

    def set_active_date_label(self):
        active_date = self.budget_database.get_current_date()
        date_text = "{day} {month} {year}".format(day=active_date[0],
                                                  month=convert_month_num(active_date[1]),
                                                  year=active_date[2])
        self.ids["active_date"].text = date_text

    def view_edit_budget(self):   
        if self.current_budget == None:
            return
        self.edit_budget_popup.open()
    
    def finish_edits(self, new_name, new_amt, new_dispamt, icon_source):
        self.current_budget.name = new_name
        self.current_budget.total = new_amt
        self.current_budget.display_total = new_dispamt

        self.budget_database.save_budget(str(self.current_budget.grid_index),
                                         new_name, new_amt, icon_source)

        self.view_budget(self.current_budget)

    def popup_add_budget(self):
        self.add_budget_popup.open()

    def add_budget(self, name, amount, icon_source, update_budgets=True):
        display_amount = '₱' + f"{amount:,.2f}"

        budget = Budget(self, self.grid_index, name,
                        display_amount, amount, icon_source)
        if update_budgets:
            self.budget_database.save_budget(str(self.grid_index),
                                             name, amount, icon_source)
        self.grid_index += 1

        self.ids["budgets_grid"].add_widget(budget)
        self.budgets_list.append(name)

    def update_icon(self, icon_source):
        self.current_budget.set_icon(icon_source)

    def view_budget(self, current_budget):
        self.current_budget = current_budget

        budget_name = self.current_budget.name
        total = self.current_budget.total

        expense = self.budget_database.get_budget_expense(budget_name)
        display_remaining = '₱' + f"{total - expense:,.2f}"

        self.ids["budget_display"].ids["budget_name"].text = \
            budget_name
        self.ids["budget_display"].ids["budget_remaining"].text = \
            display_remaining
        self.ids["budget_display"].ids["budget_total"].text = \
            self.current_budget.display_total

    def get_budgets_list(self):
        return self.budgets_list
