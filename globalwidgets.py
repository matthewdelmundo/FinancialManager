import kivy
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.properties import ColorProperty
from kivy.uix.relativelayout import RelativeLayout
from historyscreen import *

# Custom TextInput for entries
class AmountInput(TextInput):
    prepend_peso = True
    adjust_font_size = True

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
        if self.adjust_font_size:
            self.font_size = 40

    # Retrieves float amount
    def get_amount(self):
        if self.text == "":
            return 0
        return float(self.pre_period_amount + self.text[-3:])

    # Input validation for backspaces
    def do_backspace(self, from_undo=False, mode='bkspc'):
        if '.' not in self.text:
            # Reduces digit count if about-to-be-erased character is a digit
            if len(self.text) > 0 and self.text[self.cursor_index() - 1] in self.number_list:
                self.digits -= 1
            # Deletes last digit of the pre-period amount
            self.pre_period_amount = self.pre_period_amount[:-1]
            self.add_commas_to_display('delete')
            # Removes '₱' character when erasing there are no digits left
            if self.digits == 0:
                self.text = ''
            if self.adjust_font_size:
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
            if self.adjust_font_size:
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
        if self.prepend_peso:
            if mode == 'insert':
                self.text = '₱' + new_pre_period[:-1]
            else:
                self.text = '₱' + new_pre_period + '0'
        else:
            if mode == 'insert':
                self.text = new_pre_period[:-1]
            else:
                self.text = new_pre_period + '0'

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

# TODO: might delete
class CircularButton(Button):
    color = ColorProperty()

    def button_pressed(self):
        self.color = self.bg_color_down

    def button_released(self):
        self.color = self.bg_color_normal


# TODO: might delete
class RoundedButton(Button):
    color = ColorProperty()

    def button_pressed(self):
        self.color = self.bg_color_down

    def button_released(self):
        self.color = self.bg_color_normal


# TODO: Use this for custom buttons
class ImageButton(Button):
    def button_pressed(self):
        self.source = self.image_down

    def button_released(self):
        self.source = self.image_normal
